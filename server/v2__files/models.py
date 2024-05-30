from __future__ import annotations

from uuid import uuid4

from django.core import validators
from django.db import models
from v2__auth.models import User

from server.settings import AWS_BUCKET
from server.settings import storage


class File(models.Model):
    uuid = models.UUIDField(
        default=uuid4,
        primary_key=True,
        editable=False,
    )
    extension = models.CharField(max_length=8)
    domain = models.CharField(
        max_length=16,
        validators=(
            validators.MinLengthValidator(4),
            validators.RegexValidator(r'^[a-z0-9]+\Z'),
        ),
        unique=True,
        null=True,
    )
    owner = models.ForeignKey(
        to=User,
        related_name='files',
        on_delete=models.DO_NOTHING,

    )

    class Meta:
        verbose_name: str = 'Файл'
        verbose_name_plural: str = 'Файлы'

    def __str__(self) -> str:
        return self.Meta.verbose_name.lower()

    @property
    def filename(self) -> str:
        return str(self.uuid) + '.' + self.extension

    def delete(self, *args, **kwargs) -> None:
        storage.delete_object(
            Bucket=AWS_BUCKET,
            Key=self.filename,
        )
        super().delete(*args, **kwargs)
