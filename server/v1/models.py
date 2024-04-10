from typing import NoReturn
from uuid import uuid4

from django.db import models

from v1__auth.models import User


class File(models.Model):
    uuid: models.Field = models.UUIDField(primary_key=True, default=uuid4, editable=False)
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
