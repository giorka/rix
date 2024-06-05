from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from random import randint

from . import engines
from . import mongodb
from . import tasks
from server.settings import DEBUG


@dataclass
class EmailService:
    email_address: str

    @property
    def code(self) -> str:
        return ''.join(str(randint(a=0, b=9)) for _ in range(6))

    def send_code(self) -> str:
        code: str = self.code

        if DEBUG:
            logging.info(f'{code = }')

            return code

        tasks.send_message.delay(
            email_address=self.email_address,
            subject='Подтвердите действие на MyCloud',
            message='Ваш код подтверждения: ' + code,
        )

        return code


@dataclass
class Queue:
    engine: engines.MongoDBStackEngine

    class Meta:
        expire_time = timedelta(seconds=(60 * 2))

    def add(self, email_address: str) -> str:
        if self.engine.contains(document=dict(email_address=email_address)):
            return email_address

        email_service = EmailService(email_address=email_address)
        code: str = email_service.send_code()

        document = dict(
            email_address=email_address,
            code=code,
            expirationTime=datetime.utcnow() + self.Meta.expire_time,
        )

        self.engine.push(document=document)

        return email_address

    def find(self, document: dict) -> dict | None:
        return self.engine.find(document=document)

    def pop(self, _id: int) -> int:
        return self.engine.pop(_id=_id)


verification_queue = Queue(
    engine=engines.MongoDBStackEngine(collection=mongodb.verification_queue),
)
revert_queue = Queue(
    engine=engines.MongoDBStackEngine(collection=mongodb.revert_queue),
)
