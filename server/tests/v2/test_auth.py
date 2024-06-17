from __future__ import annotations

import json

import pytest
from django.urls import reverse
from faker import Faker
from rest_framework.test import APIClient

from v2__auth import models, utils


@pytest.mark.django_db()
def test_register(client: APIClient, faker: Faker) -> None:
    data = {
        'username': faker.user_name(),
        'email': faker.email(),
        'password': faker.password(length=8),
    }

    client.post(reverse('register'), data=data)

    assert models.User.objects.filter(username=data['username'], email=data['email']).exists() is True


@pytest.mark.django_db()
def test_revert(client: APIClient, faker: Faker) -> None:
    email = faker.email()

    models.User(username=faker.user_name(), email=email, is_verified=True).save()

    client.post(reverse('revert'), data={'email': email})

    assert bool(utils.email.revert_queue.find(email)) is True

    utils.email.revert_queue.flush()


@pytest.mark.django_db
def test_revert_complete(client: APIClient, faker: Faker) -> None:
    email, password = faker.email(), faker.password(length=8)

    models.User(username=faker.user_name(), email=email, is_verified=True).save()

    utils.email.revert_queue.add(email)  # TODO: возвращать документ

    code: str = utils.email.revert_queue.find(email)['code']

    response = client.post(
        reverse('revert-complete'),
        data={
            'email': email,
            'code': code,
            'new_password': password,
        },
    )

    assert json.loads(response.content).get('auth_token') is not None

    utils.email.revert_queue.flush()
