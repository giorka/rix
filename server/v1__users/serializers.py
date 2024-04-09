from typing import Tuple

from django.contrib.auth.models import AbstractUser
from rest_framework import serializers

from v1__auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields: Tuple[str] = (
            'username',
        )
        model: AbstractUser = User  # NOTE: change if another model is used
