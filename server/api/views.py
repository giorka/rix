from datetime import datetime, timedelta

from django.contrib.auth import login
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import db
from . import serializers
from . import utils


class RegisterAPIView(views.APIView):
    # permission_classes = (~IsAuthenticated,)
    serializer_class = serializers.UserRegisterFormSerializer

    class Meta:
        UNIQUE_FIELDS = (
            'username',
            'email',

        )
        DOCUMENT_EXPIRE_TIME = timedelta(seconds=(60 * 2))
        ATTEMPTS_COUNT = 3

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
        email.send_code()

        data['password'] = utils.Text(string=data['password']).encode()

        db.collection.insert_one(
            document=(
                    data
                    | dict(
                        code=email.code,
                        attemptsLeft=self.Meta.ATTEMPTS_COUNT,
                    )
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
    # permission_classes = (~IsAuthenticated,)
    user_serializer_class = serializers.UserSerializer
    user_model = user_serializer_class.Meta.model
    serializer_class = serializers.UserVerificationSerializer

    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        record = db.collection.find_one(
            dict(
                email=data.get('email')
            )
        ) or {}

        if record.get('code') != data.get('code'):
            if 'email' in record:
                if record['attemptsLeft'] == 0:
                    db.collection.delete_one({"_id": record["_id"]})

                record['attemptsLeft'] -= 1
                db.collection.replace_one({"_id": record["_id"]}, record)

            return Response(
                data=dict(
                    code=['The code has expired.']
                ),
                status=400,
            )

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
