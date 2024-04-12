from __future__ import annotations

from typing import NoReturn
from uuid import uuid4

from django.core import validators
from django.db import models
from v1__auth.models import User


class File(models.Model):
    uuid: models.Field = models.UUIDField(
        default=uuid4, primary_key=True, editable=False,
    )
    name: models.Field = models.CharField(
        max_length=16,
        validators=(
            validators.MinLengthValidator(4),
            validators.RegexValidator(r'^[a-z0-9]+\Z'),
        ),
        unique=True,
        null=True,
    )
    owner: models.Field = models.ForeignKey(
        to=User,
        related_name='files',
        on_delete=models.DO_NOTHING,

    )
    file: models.Field = models.FileField(upload_to='files/')

    class Meta:
        verbose_name: str = 'Файл'
        verbose_name_plural: str = 'Файлы'

    def __str__(self) -> str:
        return self.Meta.verbose_name.lower()

    def delete(self, *args, **kwargs) -> NoReturn:
        self.file.delete()
        super().delete(*args, **kwargs)
