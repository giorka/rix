from rest_framework import serializers


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
