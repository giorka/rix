from __future__ import annotations

from pathlib import Path
from threading import Thread
from time import sleep

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from . import utils
from server.settings import MEDIA_ROOT
from server.settings import storage

user_model: AbstractUser = get_user_model()


class FileCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.FileSerializer
    permission_classes: tuple[permissions.BasePermission] = (
        permissions.IsAuthenticated,
    )

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data, request=request)

        serializer.is_valid(raise_exception=True)

        file = serializer.save()

        return Response(data=self.serializer_class(file).data)


class FileRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.FileSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()

    @classmethod
    def get_object(cls, *args, **kwargs):
        query: str = kwargs['pk']

        user = get_object_or_404(user_model, username=kwargs['username'])

        query_type: str = (
            'uuid' if utils.is_valid_uuid(string=query)
            else 'domain'
        )  # Определяем, по какому полю идёт поиск. Принимает значения: uuid, domain.

        return get_object_or_404(cls.model, owner_id=user.id, **{query_type: query})


class FileDownloadAPIView(APIView):
    @staticmethod
    def remove_file(path: str, secs: int = 60) -> str:
        sleep(secs)

        Path(path).unlink()

        return path

    @classmethod
    def get(cls, *args, **kwargs) -> FileResponse:
        file = FileRetrieveAPIView.get_object(*args, **kwargs)

        file_name = str(file.uuid) + '.' + file.extension
        file_path = MEDIA_ROOT + '/'

        storage.get_file_by_name(file_name).download(file_or_path=file_path)

        file_href = file_path + file_name

        with open(file=file_href, mode='rb') as document:
            response = FileResponse(document)

        Thread(target=cls.remove_file, args=(file_href,)).start()

        return response
