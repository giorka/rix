from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import constants


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
        )
        model = User  # NOTE: change if another model is used


class VerifyFormSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserRegisterFormSerializer(serializers.ModelSerializer):
    code = serializers.IntegerField()

    class Meta:
        fields = (
            'username',
            'password',
            'email',
            'code',
        )
        model = User  # NOTE: change if another model is used

    def create(self, validated_data: dict) -> User:  # NOTE: change if another model is used
        obj = User.objects.create_user(
            username=validated_data.get('username'),
            password=validated_data.get('password'),
            email=validated_data.get('email'),

        )

        return obj

    def validate_code(self, speculative_code: int) -> int:
        email = self.initial_data.get('email')

        real_code = constants.redis.get(name=email).decode('utf-8')

        if not real_code or str(speculative_code) != real_code:
            seconds_left = constants.redis.ttl(name=email)
            constants.redis.expire(name=email, time=(seconds_left - 40))

            raise ValidationError('Validation error.')

        constants.redis.delete(email)

        return speculative_code
