from __future__ import annotations

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from . import serializers


class FileCreateAPIView(CreateAPIView):
    serializer_class = serializers.FileSerializer

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data, request=request)

        serializer.is_valid(raise_exception=True)

        file = serializer.save()

        return Response(data=dict(file=(file.domain or file.uuid)))
