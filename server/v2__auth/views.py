from __future__ import annotations

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from . import permissions as custom_permissions
from . import serializers
from . import utils


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.UserCreateSerializer


class RevertCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.RevertSerializer


class RevertCompleteCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.RevertCompleteSerializer


class SessionAPIView(APIView):
    permission_classes: tuple[permissions.BasePermission, ...] = (
        permissions.IsAuthenticated,
        custom_permissions.IsVerified,
    )

    @classmethod
    def post(cls, request, *args, **kwargs) -> Response:
        user_email_address: str = request.user.email

        utils.verification_queue.add(email_address=user_email_address)

        return Response(data={'email': user_email_address})


class EmailVerificationAPIView(APIView):
    serializer_class = serializers.EmailVerifySerializer
    permission_classes: tuple[permissions.BasePermission, ...] = (permissions.IsAuthenticated,)

    @classmethod
    def post(cls, request, *args, **kwargs) -> Response:
        email_address: str = request.user.email

        serializer = cls.serializer_class(
            data={
                'email': email_address,
                'code': request.data.get('code'),
            },
        )

        serializer.is_valid(raise_exception=True)

        request.user.is_verified = True
        request.user.save()

        return Response(data=serializer.validated_data)


class ChangePasswordAPIView(generics.CreateAPIView):
    serializer_class = serializers.UserChangePasswordSerializer
    permission_classes: tuple[permissions.BasePermission, ...] = (
        permissions.IsAuthenticated,
        custom_permissions.IsVerified,
    )
