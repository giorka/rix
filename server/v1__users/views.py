from typing import Tuple, Type

from django.contrib.auth.models import AbstractUser
from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.serializers import Serializer

from . import serializers


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class: Type[Serializer] = serializers.ProfileSerializer
    permission_classes: Tuple[BasePermission] = (IsAuthenticated,)

    def get_object(self) -> AbstractUser:
        return self.request.user


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class: Type[serializers.UserSerializer] = serializers.UserSerializer
    queryset: QuerySet = serializer_class.Meta.model.objects.all()
    lookup_field: str = 'username'
