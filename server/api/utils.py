from dataclasses import dataclass
from random import randint
from typing import Optional

from cryptography.fernet import Fernet

from server import settings
from . import tasks


class Email:
    def __init__(self, email_address: str):
        self.email_address: str = email_address
        self.__code: Optional[str] = None

    @property
    def code(self) -> str:
        if not self.__code:
            self.__code = ''.join((str(randint(a=0, b=9)) for _ in range(6)))

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


# def get_code() -> int:
#     return randint(a=100_000, b=999_999)
#
#
# def send_code(code: int, email_address: str):
#     """
#     TODO: загрузка с SQL и кеширование через Redis.
#     TODO: перевести сообщение на русский язык.
#     TODO: использовать celery
#     """
#
#     subject = 'Your registration code: ' + str(code)
#     message = subject + '\n' + 'If you have not registered for the service, then simply ignore this message.'
#
#     send_mail(
#         subject=subject,
#         message=message,
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[email_address]
#     )
#
#
# def get_and_send_code(email_address: str):
#     code = get_code()
#     send_code(code=code, email_address=email_address)
#
#     return code


@dataclass
class Text:
    string: str

    class Meta:
        encoding = 'UTF-8'
        key = bytes(settings.MONGO_KEY, encoding=encoding)
        fernet = Fernet(key=key)

    def encode(self) -> str:
        return self.Meta.fernet.encrypt(data=bytes(self.string, self.Meta.encoding)).decode(encoding=self.Meta.encoding)

    def decode(self) -> str:
        return self.Meta.fernet.decrypt(self.string).decode(encoding=self.Meta.encoding)
