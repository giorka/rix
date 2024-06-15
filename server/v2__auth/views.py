from __future__ import annotations

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from . import permissions as custom_permissions
from . import serializers, utils


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.UserCreateSerializer


class RevertCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.RevertSerializer


class RevertCompleteCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.RevertCompleteSerializer


class EmailVerificationAPIView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
        custom_permissions.IsVerified,
    )

    @classmethod
    def post(cls, request, *args, **kwargs) -> Response:
        user_email_address: str = request.user.email

        utils.email.verification_queue.add(user_email_address)

        return Response(data={'email': user_email_address})


class EmailVerificationCompleteAPIView(APIView):
    serializer_class = serializers.EmailVerificationCompleteSerializer
    permission_classes = (permissions.IsAuthenticated,)

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
    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        custom_permissions.IsVerified,
    )
