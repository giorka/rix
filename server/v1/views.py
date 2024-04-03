from typing import Type

from rest_framework import generics

from . import serializers


class RegisterAPIView(generics.CreateAPIView):
    serializer_class: Type[serializers.UserRegisterFormSerializer] = serializers.UserRegisterFormSerializer


class VerifyAPIView(generics.CreateAPIView):
    serializer_class: Type[serializers.UserRegisterFormSerializer] = serializers.UserVerificationSerializer
