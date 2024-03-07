from datetime import datetime, timedelta

from rest_framework import views
from rest_framework.response import Response

from . import db
from . import serializers
from . import utils


class RegisterAPIView(views.APIView):
    serializer_class = serializers.UserRegisterFormSerializer

    class Meta:
        UNIQUE_FIELDS = (
            'username',
            'email',

        )
        DOCUMENT_EXPIRE_TIME = timedelta(seconds=(60 * 2))

    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data: dict = serializer.validated_data.copy()

        for unique_field in self.Meta.UNIQUE_FIELDS:
            already_exists = db.collection.find_one({unique_field: data.get(unique_field)})

            if already_exists:
                return Response(
                    data={unique_field: [
                        'A user with that {} already exists.'.format(unique_field)
                    ]
                    },
                    status=400
                )

        email = utils.Email(email_address=data['email'])
        data['password'] = utils.Text(string=data['password']).encode()
        email.send_code()

        db.collection.insert_one(
            document=(
                    data
                    | dict(code=email.code)
                    | {'expirationTime': datetime.utcnow() + self.Meta.DOCUMENT_EXPIRE_TIME}
            )
        )

        return Response(
            data=dict(
                status=200
            ),
            status=200
        )


class VerifyAPIView(views.APIView):
    serializer_class = serializers.UserVerificationSerializer

    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        record = db.collection.find_one(
            dict(
                email=serializer.validated_data.get('email'),
                code=serializer.validated_data.get('code'),

            )
        )

        if not record:
            return Response(
                data=dict(
                    code=['The code has expired.']
                ),
                status=400,
            )



# class VerifyAPIView(views.APIView):
#     serializer_class = serializers.VerifyFormSerializer
#
#     class Meta:
#         CODE_EXPIRE_TIME = (60 * 2)
#
#     def post(self, request) -> Response:
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         email_address = serializer.validated_data['email']
#
#         if not constants.redis.get(name=email_address):
#             code = utils.get_and_send_code(email_address=email_address)
#
#             pipeline = constants.redis.pipeline()
#             pipeline.set(name=email_address, value=code)
#             pipeline.expire(name=email_address, time=self.Meta.CODE_EXPIRE_TIME)
#             pipeline.execute()
#
#         return Response(
#             data=dict(
#                 detail='OK'
#             ),
#             status=200,
#         )
#
#
# class RegisterAPIView(views.APIView):
#     serializer_class = serializers.UserRegisterFormSerializer
#
#     def post(self, request) -> Response:
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         obj = serializer.save()
#
#         return Response(
#             data=serializers.UserSerializer(obj).data
#         )
