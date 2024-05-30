from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer

from . import serializers


class UserDetailsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class: type[Serializer] = serializers.UserDetailsSerializer
    permission_classes: tuple[BasePermission] = (IsAuthenticated,)

    def get_object(self) -> AbstractUser:
        return self.request.user


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class: type[serializers.UserSerializer] = serializers.UserSerializer
    queryset: QuerySet = serializer_class.Meta.model.objects.all()
    lookup_field: str = 'username'
