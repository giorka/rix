from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core import validators
from djoser.utils import login_user as login
from rest_framework import exceptions
from rest_framework import serializers

from . import db
from server import settings


class UserCreateSerializer(serializers.ModelSerializer):
    """
    TODO: проверка почты на уникальность
    """

    auth_token: str = serializers.CharField(
        max_length=40,
        validators=(validators.MinLengthValidator(6),),
        read_only=True,
    )

    class Meta:
        model: AbstractUser = get_user_model()
        write_only_fields: tuple[str, ...] = (
            'username',
            'email',
            'password',
        )
        fields: tuple[str, ...] = (
            'auth_token',
            *write_only_fields,
        )
        extra_kwargs: dict[str, dict] = {
            field: dict(
                write_only=True,
            ) for field in write_only_fields
        }

    def create(self, validated_data: dict) -> dict:
        return (
            validated_data
            |
            dict(
                auth_token=login(
                    request=None,
                    user=self.Meta.model.objects.create_user(
                        **validated_data,
                    ),
                ),
            )
        )


class EmailVerificationSerializer(serializers.Serializer):
    email: str = serializers.EmailField()
    code: str = serializers.CharField(
        max_length=6,
        validators=(validators.MinLengthValidator(6),),
        write_only=True,
    )

    def validate_code(self, value: str) -> str:
        record: dict[str, Any] | None = db.collection.find_one(
            dict(email_address=self.initial_data['email']),
        )

        if not record:
            raise exceptions.ValidationError(
                settings.ERRORS_V2['NO_REGISTRATION_DETAILS'],
            )

        db.collection.delete_one({'_id': record['_id']})

        if value != record['code']:
            raise exceptions.ValidationError(
                settings.ERRORS_V2['NO_CORRECT_CODE'],
            )

        return value
