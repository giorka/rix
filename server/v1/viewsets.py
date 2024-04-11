from __future__ import annotations

from typing import Tuple
from typing import Type
from uuid import uuid4

from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db.models import Model
from django.db.models import QuerySet
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from . import models
from . import serializers


class AbstractViewSet(viewsets.GenericViewSet):
    class Meta:
        prefix: str = ''
        basename: str = ''


class PersonViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    AbstractViewSet,
):
    serializer_class: serializers.FileSerializer = serializers.FileSerializer
    permission_classes: tuple[permissions.BasePermission] = (
        permissions.IsAuthenticated,
    )

    class Meta:
        prefix: str = 'files'
        basename: str = 'files'

    def create(self, request: Request, *args, **kwargs) -> Response:  # Create
        serializer: serializers.serializers.Serializer = self.serializer_class(data=request.data)
        serializer.request = request
        serializer.is_valid(raise_exception=True)
        validated_data: dict = serializer.validated_data

        temporary_file: TemporaryUploadedFile = validated_data['file']
        file_name, *_, extension = temporary_file.name.split('.')
        temporary_file.name = str(uuid4()) + '.' + extension

        file: models.File = self.serializer_class.Meta.model.objects.create(**validated_data | dict(owner=request.user))

        request.user.used_memory += temporary_file.size
        request.user.save()

        return Response(
            data=self.serializer_class(
                file, context=dict(request=request),
            ).data,
        )

    @property
    def queryset(self) -> QuerySet:  # Retrieve
        return self.request.user.files.all()

    def perform_destroy(self, instance: Model) -> Response:  # Destroy
        deleted_memory: int = instance.file.size

        self.request.user.used_memory -= deleted_memory
        self.request.user.save()

        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


VIEW_SETS: tuple[type[AbstractViewSet]] = (
    PersonViewSet,
)
