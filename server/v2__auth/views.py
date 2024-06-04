from __future__ import annotations

from rest_framework import exceptions
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from . import permissions as custom_permissions
from . import serializers
from . import utils
from server import settings


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.UserCreateSerializer


class SessionAPIView(APIView):
    permission_classes: tuple[permissions.BasePermission, ...] = (permissions.IsAuthenticated,)

    @classmethod
    def post(cls, request, *args, **kwargs) -> Response:
        if request.user.is_verified:
            raise exceptions.ValidationError(settings.ERRORS_V2['NO_VERIFY_POSSIBILITY'])

        user_email_address: str = request.user.email

        email_service = utils.EmailService(email_address=user_email_address)
        code: str = email_service.send_code()

        utils.verification_queue.add(
            email_address=user_email_address,
            code=code,
        )

        return Response(data=dict(email_address=user_email_address))


class EmailVerificationAPIView(APIView):
    permission_classes: tuple[permissions.BasePermission, ...] = (permissions.IsAuthenticated,)
    serializer_class = serializers.EmailVerifySerializer

    @classmethod
    def post(cls, request, *args, **kwargs) -> Response:
        email_address: str = request.user.email

        serializer = cls.serializer_class(
            data=dict(
                email=email_address,
                code=request.data.get('code'),
            ),
        )

        serializer.is_valid(raise_exception=True)

        request.user.is_verified = True
        request.user.save()

        return Response(data=serializer.validated_data)


class ChangePasswordAPIView(generics.CreateAPIView):
    serializer_class = serializers.UserChangePasswordSerializer
    permission_classes: tuple[permissions.BasePermission, ...] = (
        permissions.IsAuthenticated,
        custom_permissions.ChangePasswordPermission,
    )
