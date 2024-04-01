from typing import Type

from django.contrib.auth import login
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from . import serializers
from .models import User


class RegisterAPIView(generics.CreateAPIView):
    serializer_class: Type[serializers.UserRegisterFormSerializer] = serializers.UserRegisterFormSerializer


class VerifyAPIView(generics.CreateAPIView):
    serializer_class: Type[serializers.UserRegisterFormSerializer] = serializers.UserVerificationSerializer

    def post(self, request, *args, **kwargs) -> Response:
        serializer_class: Serializer = self.serializer_class(data=request.data)
        serializer_class.is_valid(raise_exception=True)

        user: User = serializer_class.save()['user']
        login(request=request, user=user)

        return Response(serializer_class.validated_data)
