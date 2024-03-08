from datetime import datetime, timedelta

from django.contrib.auth import login
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import db
from . import serializers
from . import utils


class RegisterAPIView(views.APIView):
    permission_classes = (~IsAuthenticated,)
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
    permission_classes = (~IsAuthenticated,)
    user_serializer_class = serializers.UserSerializer
    user_model = user_serializer_class.Meta.model
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

        db.collection.delete_one({"_id": record["_id"]})

        user = self.user_model.objects.create_user(
            username=record.get('username'),
            password=utils.Text(record.get('password')).decode(),
            email=record.get('email'),

        )

        login(request=request, user=user)

        return Response(
            data=self.user_serializer_class(
                user
            ).data
        )
