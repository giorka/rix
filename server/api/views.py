from datetime import datetime, timedelta

from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import db
from . import serializers
from . import utils


class RegisterAPIView(views.APIView):
    """
    Добавляет пользователя в очередь на регистрацию и генерирует код подтверждения.
    Код подтверждения отправляется на почту.
    Для регистрации пользователя нужно отправить POST на v1/verify/.
    (будут использованы данные, отправленные на v1/register/)
    """

    permission_classes = (~IsAuthenticated,)
    serializer_class = serializers.UserRegisterFormSerializer

    class Meta:
        UNIQUE_FIELDS = (
            'username',
            'email',

        )
        DOCUMENT_EXPIRE_TIME = timedelta(seconds=(60 * 2))
        ATTEMPTS_COUNT = 3

    @method_decorator(ratelimit(key='ip', rate='1/m'))
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
        print(email.code)
        # email.send_code()

        data['password'] = utils.Text(string=data['password']).encode()

        db.collection.insert_one(
            document=(
                    data
                    | dict(code=email.code, attemptsLeft=self.Meta.ATTEMPTS_COUNT)
                    | {'expirationTime': datetime.utcnow() + self.Meta.DOCUMENT_EXPIRE_TIME}
            )
        )

        return Response(
            data=dict(
                status=200
            ),
            status=201
        )


class VerifyAPIView(views.APIView):
    """
    POST /v1/verify/ {'email': 'example@example.com', 'code': '123456'}
    NOTE: Код передается строкой. Содержит 6 символов. Интервал: 000000 — 999999.
    
    — Принцип работы
    А) Принимает почту и код.
    Б) Ищет почту в очереди.
    В)
        1) Есть в очереди:
             А) Кончились попытки: Ответ {'detail': 'Attempts have expired.'} с кодом 429.
             Б) Уменьшает кол-во попыток.
             В)
                1) Код из БД = предоставленный код: Регистрация пользователя.
                2) Код из БД != предоставленный код: Ответ {detail: 'The code has expired.'} с кодом 422.
        2) Нет в очереди: Ответ {detail: 'Registration details not found.'} с кодом 422.
    """

    permission_classes = (~IsAuthenticated,)
    user_serializer_class = serializers.UserSerializer
    user_model = user_serializer_class.Meta.model
    serializer_class = serializers.UserVerificationSerializer

    @method_decorator(ratelimit(key='ip', rate='1/m'))
    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        record = db.collection.find_one(
            dict(
                email=data.get('email')
            )
        ) or {}

        if 'email' in record:  # если есть в очереди
            if record['attemptsLeft'] == 0:  # если нет попыток
                db.collection.delete_one({"_id": record["_id"]})  # удаляем из очереди

                return Response(
                    data=dict(
                        detail='Attempts have expired.'
                    ),
                    status=429,
                )

            if record.get('code') != data.get('code'):  # если код не совпадает
                record['attemptsLeft'] -= 1  # сокращаем кол-во попыток на 1
                db.collection.replace_one({"_id": record["_id"]}, record)  # сохраняем в БД

                return Response(
                    data=dict(
                        detail='The code has expired.'
                    ),
                    status=422,
                )
        else:  # если нет в очереди
            return Response(
                data=dict(
                    detail='Registration details not found.'
                ),
                status=422,
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
            ).data,
            status=200,
        )
