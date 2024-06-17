from __future__ import annotations

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
