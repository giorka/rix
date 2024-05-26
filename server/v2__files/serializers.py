from __future__ import annotations

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.uploadedfile import TemporaryUploadedFile
from rest_framework import exceptions
from rest_framework import serializers
from rest_framework.request import Request
from v2__auth.serializers import UserSerializer

from . import models
from server.settings import ERRORS_V2
from server.settings import MAX_USER_DOMAIN
from server.settings import storage


class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = models.File
        fields = '__all__'

    def __init__(self, *args, request: Request = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.request: Request | None = request  # POST — Request; GET — None;

    def create(self, validated_data: dict) -> models.File:
        temporary_file: TemporaryUploadedFile = validated_data['file']

        file: models.File = self.Meta.model.objects.create(
            domain=(
                validated_data.get('domain')
                if self.request.user.is_premium_user else None
            ),
            owner=self.request.user,
        )

        self.request.user.used_memory += temporary_file.size
        self.request.user.save()

        _, extension = str(temporary_file).split('.')

        storage.upload(
            file=temporary_file.file,
            file_name=str(file.uuid) + '.' + extension,
        )

        return file

    def validate_file(self, file: InMemoryUploadedFile) -> InMemoryUploadedFile:
        if (self.request.user.files.count() + 1) > self.request.user.max_files:
            raise exceptions.ValidationError(ERRORS_V2['NO_FILES_SLOTS'])
        elif (self.request.user.used_memory + file.size) > self.request.user.max_memory:
            raise exceptions.ValidationError(ERRORS_V2['NO_MEMORY'])
        elif 'domain' in self.initial_data and (self.request.user.domains + 1) > MAX_USER_DOMAIN:
            raise exceptions.ValidationError(ERRORS_V2['NO_DOMAINS_SLOTS'])

        return file
