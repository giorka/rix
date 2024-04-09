from typing import Tuple

from django.contrib.auth.models import AbstractUser
from rest_framework import serializers

from v1__auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model: AbstractUser = User  # NOTE: change if another model is used
        fields: Tuple[str, ...] = (
            'username',
        )


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model: AbstractUser = UserSerializer.Meta.model
        fields: Tuple[str, ...] = (
            *UserSerializer.Meta.fields,
            'email',

        )
