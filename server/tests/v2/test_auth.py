from __future__ import annotations

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from tests import constants
from v2__auth import models


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
