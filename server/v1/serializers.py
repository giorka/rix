from __future__ import annotations

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request

from . import models
from server import settings


class FileSerializer(serializers.ModelSerializer):
    owner: serializers.Field = serializers.SerializerMethodField()

    class Meta:
        model: models.models.Model = models.File
        fields: str = '__all__'
        read_only_fields = ('owner',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request: Request | None = None

    def validate_file(self, obj: InMemoryUploadedFile) -> InMemoryUploadedFile:
        if (obj.size + self.request.user.used_memory) > settings.MAX_USER_MEMORY:
            raise ValidationError(
                'Превышено максимальное количество выделенной памяти для пользователя.',
            )

        return obj

    @staticmethod
    def get_owner(obj: models.File) -> str:
        return str(obj.owner)
