from datetime import datetime, timedelta
from typing import NoReturn, Optional, Tuple

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from djoser.utils import login_user as login
from rest_framework import fields
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from server.settings import DEBUG
from . import db, utils
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields: Tuple[str] = (
            'username',
        )
        model: AbstractUser = User  # NOTE: change if another model is used


class UserRegisterFormSerializer(serializers.ModelSerializer):
    email: fields.EmailField = fields.EmailField()

    class Meta:
        fields: Tuple[str] = (
            'username',
            'password',
            'email',
        )
        model: AbstractUser = User  # NOTE: change if another model is used

    class Settings:
        UNIQUE_FIELDS: Tuple[str] = (
            'username',
            'email',

        )
        DOCUMENT_EXPIRE_TIME: timedelta = timedelta(seconds=(60 * 2))
        ATTEMPTS_COUNT: int = 3

    def validate(self, attrs: dict) -> dict:
        """
        Проверяет, есть ли уникальные поля в MongoDB очереди на регистрацию
        """

        super().validate(attrs=attrs)

        for unique_field in self.Settings.UNIQUE_FIELDS:
            already_exists: Optional[dict] = db.collection.find_one(
                {unique_field: attrs.get(unique_field)}
            )

            if already_exists:
                raise ValidationError('A user with that {} already exists.'.format(unique_field))

        return attrs

    def validate_email(self, value: str) -> str:
        """
        Проверяет, зарегистрирован ли пользователь с таким же Email адресом
        """

        if self.Meta.model.objects.filter(email=value).exists():
            raise ValidationError('A user with that email already exists.')

        return value

    def create(self, validated_data: dict) -> dict:
        email: utils.Email = utils.Email(email_address=validated_data['email'])
        code: str = email.code

        if DEBUG:
            print(code)
        else:
            email.send_code()

        data: dict = validated_data.copy()
        data['password']: str = utils.Text(string=data['password']).encode()

        db.collection.insert_one(
            document=(
                    data
                    | dict(code=email.code, attemptsLeft=self.Settings.ATTEMPTS_COUNT)
                    | dict(expirationTime=datetime.utcnow() + self.Settings.DOCUMENT_EXPIRE_TIME)
            )
        )

        return validated_data


class UserVerificationSerializer(serializers.Serializer):
    auth_token: serializers.CharField = serializers.CharField(
        max_length=40,
        validators=(
            MinLengthValidator(6),
        ),
        read_only=True
    )
    email: serializers.EmailField = serializers.EmailField(write_only=True)
    code: serializers.CharField = serializers.CharField(
        max_length=6,
        validators=(
            MinLengthValidator(6),
        ),
        write_only=True
    )

    class Meta:
        model: AbstractUser = User

    def __init__(self, *args, **kwargs) -> NoReturn:
        super().__init__(*args, **kwargs)
        self._record: Optional[dict] = None

    def validate(self, attrs: dict) -> dict:
        if not self._record:
            raise ValidationError('Registration details not found.')
        elif self._record['attemptsLeft'] == 0:
            db.collection.delete_one({"_id": self._record["_id"]})

            raise ValidationError('Attempts have expired.')

        return attrs

    def validate_email(self, value: str) -> str:
        self._record: dict = db.collection.find_one(dict(email=value))

        return value

    def validate_code(self, value: str) -> str:
        if not self._record:
            return value

        if self._record['code'] != value:
            self._record['attemptsLeft'] -= 1
            db.collection.replace_one({"_id": self._record["_id"]}, self._record)

            raise ValidationError('Invalid secret key.')

        return value

    def create(self, validated_data: dict) -> dict:
        db.collection.delete_one({"_id": self._record["_id"]})

        user: AbstractUser = self.Meta.model.objects.create_user(
            username=self._record['username'],
            email=self._record['email'],
            password=utils.Text(string=self._record['password']).decode(),
        )

        auth_token: str = login(request=None, user=user)

        return validated_data | dict(auth_token=auth_token)
