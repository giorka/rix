from rest_framework import serializers

from . import models


class FileSerializer(serializers.ModelSerializer):
    owner: serializers.Field = serializers.SerializerMethodField()

    class Meta:
        model: models.models.Model = models.File
        fields: str = '__all__'
        read_only_fields = ('owner',)

    @staticmethod
    def get_owner(obj: models.File) -> str:
        return str(obj.owner)
