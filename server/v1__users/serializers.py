from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model: AbstractUser = get_user_model()  # NOTE: change if another model is used
        fields: tuple[str, ...] = (
            'username',
            'is_premium_user',
        )


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model: AbstractUser = UserSerializer.Meta.model
        fields: tuple[str, ...] = (
            *UserSerializer.Meta.fields,
            'email',
        )
