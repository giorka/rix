from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
        )
        model = User  # NOTE: change if another model is used


class UserRegisterFormSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'password',
            'email',
        )
        model = User  # NOTE: change if another model is used


class UserVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(
        max_length=6,
        validators=(
            MinLengthValidator(6),
        )
    )

    # def validate_code(self, speculative_code: int) -> int:
    #     email = self.initial_data.get('email')
    #
    #     real_code = constants.redis.get(name=email).decode('utf-8')
    #
    #     if not real_code or str(speculative_code) != real_code:
    #         seconds_left = constants.redis.ttl(name=email)
    #         constants.redis.expire(name=email, time=(seconds_left - 40))
    #
    #         raise ValidationError('Validation error.')
    #
    #     constants.redis.delete(email)
    #
    #     return speculative_code

# class UserRegisterFormSerializer(serializers.ModelSerializer):
#     code = serializers.IntegerField()
#
#     class Meta:
#         fields = (
#             'username',
#             'password',
#             'email',
#             'code',
#         )
#         model = User  # NOTE: change if another model is used
#
#     def create(self, validated_data: dict) -> User:  # NOTE: change if another model is used
#         obj = User.objects.create_user(
#             username=validated_data.get('username'),
#             password=validated_data.get('password'),
#             email=validated_data.get('email'),
#
#         )
#
#         return obj
#
#     def validate_code(self, speculative_code: int) -> int:
#         email = self.initial_data.get('email')
#
#         real_code = constants.redis.get(name=email).decode('utf-8')
#
#         if not real_code or str(speculative_code) != real_code:
#             seconds_left = constants.redis.ttl(name=email)
#             constants.redis.expire(name=email, time=(seconds_left - 40))
#
#             raise ValidationError('Validation error.')
#
#         constants.redis.delete(email)
#
#         return speculative_code

# class VerifyFormSerializer(serializers.Serializer):
#     email = serializers.EmailField()
