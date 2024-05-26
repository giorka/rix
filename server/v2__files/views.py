from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response

from . import serializers
from . import utils

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

    def get_object(self, *args, **kwargs):
        query: str = self.kwargs['pk']

        user = get_object_or_404(user_model, username=self.kwargs['username'])

        query_type: str = (
            'uuid' if utils.is_valid_uuid(string=query)
            else 'domain'
        )  # Определяем, по какому полю идёт поиск. Принимает значения: uuid, domain.

        return get_object_or_404(self.model, owner_id=user.id, **{query_type: query})
