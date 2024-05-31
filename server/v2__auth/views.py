from __future__ import annotations

from datetime import datetime
from datetime import timedelta

from rest_framework import exceptions
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from . import db
from . import permissions as custom_permissions
from . import serializers
from . import utils
from server import settings


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.UserCreateSerializer


class SessionAPIView(APIView):
    permission_classes: tuple[permissions.BasePermission, ...] = (
        permissions.IsAuthenticated,
    )

    class Settings:
        DOCUMENT_EXPIRE_TIME: timedelta = timedelta(seconds=(60 * 2))

    def post(self, request, *args, **kwargs) -> Response:
        # переделать в @classmethod
        if request.user.is_verified:
            raise exceptions.ValidationError(
                settings.ERRORS_V2['NO_VERIFY_POSSIBILITY'],
            )

        email_address: str = request.user.email

        record: dict | None = db.collection.find_one(
            filter=dict(
                email_address=email_address,
            ),
        )

        if record:
            return Response(data=dict(email=email_address), status=200)

        email: utils.Email = utils.Email(email_address=email_address)
        code: str = email.code

        if settings.DEBUG:
            print(code)
        else:
            email.send_code()

        db.collection.insert_one(
            document=dict(
                email_address=email_address,
                code=email.code,
                expirationTime=datetime.utcnow() + self.Settings.DOCUMENT_EXPIRE_TIME,
            ),
        )

        return Response(data=dict(email=email_address), status=200)


class EmailVerificationAPIView(APIView):
    permission_classes: tuple[permissions.BasePermission, ...] = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.EmailVerifySerializer

    def post(self, request, *args, **kwargs) -> Response:
        # TODO: переделать в @classmethod
        email_address: str = request.user.email

        serializer = self.serializer_class(
            data=dict(
                email=email_address,
                **request.data,
            ),
        )

        serializer.is_valid(raise_exception=True)

        self.request.user.is_verified = True
        self.request.user.save()

        return Response(data=serializer.validated_data)


class ChangePasswordAPIView(generics.CreateAPIView):
    serializer_class = serializers.UserChangePasswordSerializer
    permission_classes: tuple[permissions.BasePermission, ...] = (
        permissions.IsAuthenticated,
        custom_permissions.ChangePasswordPermission,
    )
