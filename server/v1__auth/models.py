# from __future__ import annotations
#
# from django.contrib.auth.models import AbstractUser
# from django.db import models
#
# from server import settings
#
#
# class User(AbstractUser):
#     first_name = last_name = None  # Удаляем поля
#     is_premium_user: bool = models.BooleanField(default=False)
#     used_memory: int = models.IntegerField(
#         default=0,
#     )  # NOTE: Записано в байтах
#
#     class Meta:
#         verbose_name: str = 'Пользователь'
#         verbose_name_plural: str = 'Пользователи'
#
#     def __str__(self) -> str:
#         return self.Meta.verbose_name.lower()
#
#     @property
#     def domains(self):
#         return self.files.filter(domain__isnull=False).count()
#
#     @property
#     def max_memory(self) -> int:
#         return (
#             settings.MAX_USER_MEMORY
#             if not self.is_premium_user
#             else settings.MAX_PREMIUM_USER_MEMORY
#         )
#
#     @property
#     def max_files(self) -> int:
#         return (
#             settings.MAX_USER_FILES
#             if not self.is_premium_user
#             else settings.MAX_PREMIUM_USER_FILES
#         )
from __future__ import annotations
