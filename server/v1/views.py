from typing import Type

from django.contrib.auth.models import AbstractUser
from djoser.utils import login_user as login
from rest_framework import generics
from rest_framework.request import Request

from . import serializers


class RegisterAPIView(generics.CreateAPIView):
    serializer_class: Type[serializers.UserRegisterFormSerializer] = serializers.UserRegisterFormSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.create(validated_data=serializer.validated_data)


class VerifyAPIView(generics.CreateAPIView):
    serializer_class: Type[serializers.UserRegisterFormSerializer] = serializers.UserVerificationSerializer

    def create(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: AbstractUser = serializer.create(validated_data=serializer.validated_data)
        token: str = login(request=request, user=user)

        return serializer.validated_data | dict(token=str(token))

    # def post(self, request, *args, **kwargs) -> Response:
    #     serializer_class: Serializer = self.serializer_class(data=request.data)
    #     serializer_class.is_valid(raise_exception=True)
    #
    #     user: User = serializer_class.save()['user']
    #     login(request=request, user=user)
    #
    #     return Response(serializer_class.validated_data)
