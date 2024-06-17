from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from random import randint

from server.settings import DEBUG
from v2__auth import engines, mongodb, tasks


@dataclass
class EmailService:
    email_address: str

    @staticmethod
    def generate_code() -> str:
        return ''.join(str(randint(a=0, b=9)) for _ in range(6))

    def send_code(self) -> str:
        code: str = self.generate_code()

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
class EmailQueue:
    engine: engines.BaseStackEngine

    class Meta:
        expire_time = timedelta(seconds=(60 * 2))

    def __getattr__(self, item: str) -> callable:
        return getattr(self.engine, item)

    def add(self, email: str) -> dict:
        existing_document: dict | None = self.engine.find(document={'email': email})

        if bool(existing_document):
            return existing_document

        email_service = EmailService(email_address=email)
        code: str = email_service.send_code()

        document = {
            'email': email,
            'code': code,
            'expirationTime': datetime.utcnow() + self.Meta.expire_time,
        }

        self.engine.push(document=document)

        return document

    def find(self, email: str) -> dict | None:
        return self.engine.find(document={'email': email})

    def is_valid_code(self, email: str, excepted_code: str) -> bool:
        record = self.find(email)

        if not record:
            return False

        self.pop(record['_id'])

        if excepted_code != record['code']:
            return False

        return True


verification_queue = EmailQueue(engine=engines.MongoDBStackEngine(collection=mongodb.verification_queue))
revert_queue = EmailQueue(engine=engines.MongoDBStackEngine(collection=mongodb.revert_queue))
