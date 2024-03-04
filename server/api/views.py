from rest_framework import views
from rest_framework.response import Response

from . import constants
from . import serializers
from . import utils


class VerifyAPIView(views.APIView):
    serializer_class = serializers.VerifyFormSerializer

    class Meta:
        CODE_EXPIRE_TIME = (60 * 2)

    def post(self, request) -> Response:
        """
        TODO: если есть уже код, то не делать нечего
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email_address = serializer.validated_data['email']

        if not constants.redis.get(name=email_address):
            code = utils.get_and_send_code(email_address=email_address)

            pipeline = constants.redis.pipeline()
            pipeline.set(name=email_address, value=code)
            pipeline.expire(name=email_address, time=self.Meta.CODE_EXPIRE_TIME)
            pipeline.execute()

        return Response(
            data=dict(
                detail='OK'
            ),
            status=200,
        )


class RegisterAPIView(views.APIView):
    serializer_class = serializers.UserRegisterFormSerializer

    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()

        return Response(
            data=serializers.UserSerializer(obj).data
        )
