from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models

from server import settings


class User(AbstractUser):
    first_name = last_name = None  # Удаляем поля
    is_premium_user: models.Field = models.BooleanField(default=False)
    used_memory: models.Field = models.IntegerField(
        default=0,
    )  # NOTE: Записано в байтах

    class Meta:
        verbose_name: str = 'Пользователь'
        verbose_name_plural: str = 'Пользователи'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._max_memory: int | None = None

    def __str__(self) -> str:
        return self.Meta.verbose_name.lower()

    @property
    def max_memory(self) -> int:
        if not self._max_memory:
            self._max_memory = (
                settings.MAX_USER_MEMORY
                if not self.is_premium_user
                else settings.MAX_PREMIUM_USER_MEMORY
            )

        return self._max_memory
