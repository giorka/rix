from __future__ import annotations

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from tests import constants
from v2__auth import models
from v2__auth import utils


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
def test_revert(client: APIClient, username: str, email: str, status_code: int) -> None:
    is_going_correct = status_code == 201

    models.User(username=username, email=email, is_verified=is_going_correct).save()

    response = client.post(reverse('revert'), data={'email': email})

    assert response.status_code == status_code
    assert bool(utils.email.revert_queue.find(email)) is is_going_correct
