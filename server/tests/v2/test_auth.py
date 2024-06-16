from __future__ import annotations

import json

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from tests import constants
from v2__auth import models, utils


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('username', 'email', 'password', 'status_code'),
    (
        (constants.faker.user_name(), constants.faker.email(), constants.faker.password(length=8), 201),
        ('taken_username', constants.faker.email(), constants.faker.password(length=8), 400),
        (constants.faker.user_name(), 'invalid_email', constants.faker.password(length=8), 400),
        (constants.faker.user_name(), constants.faker.email(), '123', 400),
    ),
)
def test_register(client: APIClient, username: str, email: str, password: str, status_code: int) -> None:
    models.User(username='taken_username').save()

    response = client.post(
        reverse('register'),
        data={
            'username': username,
            'email': email,
            'password': password,
        },
    )

    assert response.status_code == status_code
    assert models.User.objects.filter(username=username, email=email).exists() is (status_code == 201)


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('username', 'email', 'status_code'),
    (
        (constants.faker.user_name(), constants.faker.email(), 201),
        (constants.faker.user_name(), 'not_verified@gmail.com', 404),
        (constants.faker.user_name(), 'nonexistent@gmail.com', 404),
    ),
)
def test_revert(
    client: APIClient,
    username: str,
    email: str,
    status_code: int,
) -> None:
    is_going_correct = status_code == 201

    models.User(username=username, email=email, is_verified=is_going_correct).save()

    response = client.post(reverse('revert'), data={'email': email})

    assert response.status_code == status_code
    assert bool(utils.email.revert_queue.find(email)) is is_going_correct

    utils.email.revert_queue.flush()


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('username', 'email', 'password', 'status_code'),
    (
        (constants.faker.user_name(), constants.faker.email(), constants.faker.password(length=8), 201),
        (constants.faker.user_name(), constants.faker.email(), constants.faker.password(length=8), 404),
        (constants.faker.user_name(), constants.faker.email(), constants.faker.password(length=8), 400),
    ),
)
def test_revert_complete(
    client: APIClient,
    username: str,
    email: str,
    password: str,
    status_code: int,
) -> None:
    if status_code != 404:
        models.User(username=username, email=email, is_verified=True).save()

    utils.email.revert_queue.add(email)

    code: str = utils.email.revert_queue.find(email)['code']

    if status_code == 400:
        invalid_code: str = utils.email.EmailService.generate_code()

        while invalid_code == code:
            invalid_code = utils.email.EmailService.generate_code()

        code = invalid_code

    response = client.post(
        reverse('revert-complete'),
        data={
            'email': email,
            'code': code,
            'new_password': password,
        },
    )

    assert response.status_code == status_code

    if status_code == 201:
        assert json.loads(response.content).get('auth_token') is not None

    utils.email.revert_queue.flush()
