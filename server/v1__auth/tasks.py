from __future__ import annotations

from celery import shared_task
from django.core.mail import send_mail

from server import settings


@shared_task
def send_message(email_address: str, subject: str, message: str):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email_address],
    )
