from rest_framework import views
from rest_framework.response import Response

from . import constants
from . import serializers
from . import utils


class VerifyAPIView(views.APIView):
    serializer_class = serializers.VerifyFormSerializer

    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email_address = serializer.validated_data['email']
        code = utils.get_and_send_code(email_address=email_address)

        constants.redis.set(name=email_address, value=code)

        return Response(
            data=dict(
                detail='OK'
            ),
            status=200,
        )


class RegisterAPIView(views.APIView):
    """
    TODO: реализовать регистрацию
    """

    def post(self, request) -> Response:
        ...
