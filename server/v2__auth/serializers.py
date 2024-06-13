from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password
from django.core import validators
from djoser.utils import login_user as login
from rest_framework import exceptions
from rest_framework import serializers
from v2.utils.orm import get_object_or_404

from . import utils
from server import settings

user_model: AbstractUser = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model: AbstractUser = user_model
        fields = (
            'username',
            'is_staff',
            'is_verified',
            'is_premium_user',
        )


class DetailedUserSerializer(UserSerializer):
    max_memory = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + (
            'used_memory',
            'max_memory',
        )

    @staticmethod
    def get_max_memory(*_) -> int:
        return settings.MAX_USER_MEMORY


class UserCreateSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(
        max_length=40,
        validators=(validators.MinLengthValidator(6),),
        read_only=True,
    )

    class Meta:
        model: AbstractUser = user_model
        write_only_fields = (
            'username',
            'email',
            'password',
        )
        fields = (
            'auth_token',
            *write_only_fields,
        )
        extra_kwargs: dict[str, dict] = {field: {'write_only': True} for field in write_only_fields}

    @staticmethod
    def validate_password(value: str) -> str:
        validate_password(value)

        return value

    def create(self, validated_data: dict) -> dict:
        return validated_data | {
            'auth_token': login(request=None, user=self.Meta.model.objects.create_user(**validated_data)),
        }


class RevertSerializer(serializers.Serializer):
    email = serializers.EmailField()

    @staticmethod
    def validate_email(value: str) -> str:
        get_object_or_404(user_model, email=value, is_verified=True)

        return value

    def save(self, **kwargs) -> None:
        utils.email.revert_queue.add(self.validated_data['email'])


class EmailCodeRequirementSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(
        max_length=6,
        validators=(validators.MinLengthValidator(6),),
        write_only=True,
    )

    class Meta:
        queue: utils.email.EmailQueue = ...

    def validate_code(self, value: str) -> str:
        email: str = self.initial_data['email']

        if self.Meta.queue.is_valid_code(email, excepted_code=value):
            return value
        else:
            raise exceptions.ValidationError(settings.ERRORS_V2['NO_CORRECT_CODE'])


class RevertCompleteSerializer(EmailCodeRequirementSerializer):
    auth_token = serializers.CharField(
        max_length=40,
        validators=(validators.MinLengthValidator(6),),
        read_only=True,
    )
    email = serializers.EmailField(write_only=True)
    new_password = serializers.CharField(validators=(validate_password,), write_only=True)

    class Meta:
        queue = utils.email.revert_queue

    def create(self, validated_data: dict) -> dict:
        user = get_object_or_404(user_model, email=self.validated_data['email'], is_verified=True)
        utils.auth.cp(user, new_password=self.validated_data['new_password'])

        return {'auth_token': str(login(request=None, user=user))}


class EmailVerificationCompleteSerializer(EmailCodeRequirementSerializer):
    class Meta:
        queue = utils.email.verification_queue

    @staticmethod
    def validate_email(value: str) -> str:
        if user_model.objects.filter(email=value, is_verified=True).exists():
            raise exceptions.ValidationError(settings.ERRORS_V2['NO_VERIFY_SLOTS'])

        return value


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(validators=(validate_password,))
    new_password = serializers.CharField(validators=(validate_password,))

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._user: AbstractUser | None = None

    def validate_password(self, value: str) -> str:
        self._user: AbstractUser = self.context['request'].user

        if not self._user.check_password(raw_password=value):
            raise exceptions.ValidationError('The password is incorrect.')

        return value

    def save(self, **kwargs) -> None:
        utils.auth.cp(self._user, new_password=self.validated_data['new_password'])
