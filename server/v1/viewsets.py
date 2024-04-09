from typing import Tuple
from uuid import uuid4

from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db.models import QuerySet
from rest_framework import mixins, permissions, viewsets
from rest_framework.response import Response

from . import serializers


class PersonViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class: serializers.FileSerializer = serializers.FileSerializer
    permission_classes: Tuple[permissions.BasePermission] = (
        permissions.IsAuthenticated,
    )

    def create(self, request, *args, **kwargs) -> Response:
        serializer: serializers.serializers.Serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data: dict = serializer.validated_data

        temporary_file: TemporaryUploadedFile = validated_data['file']
        file_name, extension = temporary_file.name.split('.')
        temporary_file.name = str(uuid4()) + '.' + extension

        self.serializer_class.Meta.model.objects.create(**(validated_data | dict(owner=request.user)))

        return Response(data=dict(file=file_name + '.' + extension))

    @property
    def queryset(self) -> QuerySet:
        return self.request.user.files.all()
