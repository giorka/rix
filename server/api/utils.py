from django.core.mail import send_mail

from ..server.settings import EMAIL_HOST_USER


def send_code(code: int, email_address: str):
    subject = 'Your registration code: ' + str(code)
    message = subject + '\n' + 'If you have not registered for the service, then simply ignore this message.'

    send_mail(
        subject=subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email_address]
    )
