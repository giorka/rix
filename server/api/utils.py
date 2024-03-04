from os import getenv
from random import randint

from django.core.mail import send_mail
from dotenv import load_dotenv

load_dotenv()  # loads .env


def get_code() -> int:
    return randint(a=100_000, b=999_999)


def send_code(code: int, email_address: str):
    """
    TODO: загрузка с SQL и кеширование через Redis.
    TODO: перевести сообщение на русский язык.
    TODO: использовать celery
    """

    subject = 'Your registration code: ' + str(code)
    message = subject + '\n' + 'If you have not registered for the service, then simply ignore this message.'

    send_mail(
        subject=subject,
        message=message,
        from_email=getenv(key='EMAIL_HOST_USER'),
        recipient_list=[email_address]
    )


def get_and_send_code(email_address: str):
    code = get_code()
    send_code(code=code, email_address=email_address)

    return code
