from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from djoser.conf import settings as djoser_settings


def logout(user: AbstractUser) -> AbstractUser:
    djoser_settings.TOKEN_MODEL.objects.filter(user=user).delete()

    return user


def cp(user: AbstractUser, new_password: str) -> str:
    logout(user)
    user.set_password(new_password)
    user.save()

    return new_password
