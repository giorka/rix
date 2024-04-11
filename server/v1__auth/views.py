from __future__ import annotations

from typing import Type

from rest_framework import generics

from . import serializers


class RegisterAPIView(generics.CreateAPIView):
    serializer_class: type[serializers.UserRegisterFormSerializer] = serializers.UserRegisterFormSerializer


class VerifyAPIView(generics.CreateAPIView):
    serializer_class: type[serializers.UserVerificationSerializer] = serializers.UserVerificationSerializer
