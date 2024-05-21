from __future__ import annotations

from random import randint

from . import tasks


class Email:
    def __init__(self, email_address: str):
        self.email_address: str = email_address
        self.__code: str | None = None

    @property
    def code(self) -> str:
        if not self.__code:
            self.__code = ''.join(str(randint(a=0, b=9)) for _ in range(6))

        return self.__code

    def send_message(self, subject: str, message: str):
        tasks.send_message.delay(
            email_address=self.email_address,
            subject=subject,
            message=message,
        )

    def send_code(self):
        self.send_message(
            subject='Подтвердите регистрацию на MyCloud',
            message='Ваш код подтверждения: ' + self.code,
        )
