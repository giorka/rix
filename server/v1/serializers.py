from __future__ import annotations

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request

from . import models
from server.settings import ERRORS
from server.settings import MAX_USER_DOMAIN


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
        if (self.request.user.files.count() + 1) > self.request.user.max_files:
            raise ValidationError(
                ERRORS['NO_FILES_SLOTS'],
            )
        elif (self.request.user.used_memory + obj.size) > self.request.user.max_memory:
            raise ValidationError(
                ERRORS['NO_MEMORY'],
            )
        elif 'domain' in self.initial_data and (self.request.user.domains + 1) > MAX_USER_DOMAIN:
            raise ValidationError(
                ERRORS['NO_DOMAINS_SLOTS'],
            )

        return obj

    @staticmethod
    def get_owner(obj: models.File) -> str:
        return obj.owner.username
