from __future__ import annotations

from rest_framework import generics

from . import serializers


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = serializers.UserRegisterFormSerializer


class VerifyAPIView(generics.CreateAPIView):
    serializer_class = serializers.UserVerificationSerializer
