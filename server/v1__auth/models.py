from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = last_name = None  # Удаляем поля
    used_memory: models.Field = models.IntegerField(default=0)  # NOTE: Записано в байтах

    class Meta:
        verbose_name: str = 'Пользователь'
        verbose_name_plural: str = 'Пользователи'

    def __str__(self) -> str:
        return self.Meta.verbose_name.lower()
