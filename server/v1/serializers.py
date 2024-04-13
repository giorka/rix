from __future__ import annotations

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request

from . import models
from server.settings import ERRORS
from server.settings import MAX_PREMIUM_USER_FILES_COUNT
from server.settings import MAX_USER_FILES_COUNT


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
        if self.request.user.files.count() >= (
                MAX_USER_FILES_COUNT
                if not self.request.user.is_premium_user
                else MAX_PREMIUM_USER_FILES_COUNT
        ):
            raise ValidationError(
                ERRORS['NO_FILES_SLOTS'],
            )
        elif (obj.size + self.request.user.used_memory) > self.request.user.max_memory:
            raise ValidationError(
                ERRORS['NO_MEMORY'],
            )

        return obj

    @staticmethod
    def get_owner(obj: models.File) -> str:
        return obj.owner.username
