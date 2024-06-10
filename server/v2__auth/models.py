from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models

from server import settings


class User(AbstractUser):
    first_name = last_name = None  # Удаляем поля
    email = models.EmailField(blank=False)
    is_verified = models.BooleanField(default=False)
    is_premium_user = models.BooleanField(default=False)
    used_memory = models.IntegerField(
        default=0,
    )  # NOTE: Записано в байтах

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.Meta.verbose_name.lower()

    @property
    def domains(self):
        return self.files.filter(domain__isnull=False).count()

    @property
    def max_memory(self) -> int:
        return settings.MAX_USER_MEMORY if not self.is_premium_user else settings.MAX_PREMIUM_USER_MEMORY

    @property
    def max_files(self) -> int:
        return settings.MAX_USER_FILES if not self.is_premium_user else settings.MAX_PREMIUM_USER_FILES
