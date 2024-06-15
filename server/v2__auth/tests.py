from __future__ import annotations

import json

from django.urls import reverse
from rest_framework.test import APITestCase

from v2.utils import tests as tests_utils

from . import models, utils
from .utils import email as email_utils


class UserCreateTestCase(APITestCase):
    client_class = tests_utils.LoggerAPIClient
    path = reverse('register')

    def test_all_ok(self) -> None:
        """
        Test to verify that an API works with correct data.
        """

        data = {
            'username': 'test',
            'email': 'good_email@gmail.com',
            'password': '123456789good_password$',
        }

        response = self.client.post(self.path, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(models.User.objects.filter(username=data['username'], email=data['email']).exists())

    def test_taken_username(self) -> None:
        """
        Test to verify that an API does not work with taken usernames.
        """

        data = {
            'username': 'taken_username',
            'email': 'good_email@gmail.com',
            'password': '123456789good_password$',
        }

        models.User(username='taken_username').save()

        response = self.client.post(self.path, data=data)

        self.assertEqual(response.status_code, 400)

    def test_invalid_email(self) -> None:
        """
        Test to verify that an API does not work with invalid emails.
        """

        data = {
            'username': 'test',
            'email': 'invalid_email',
            'password': '123456789good_password$',
        }

        response = self.client.post(self.path, data=data)

        self.assertEqual(response.status_code, 400)

    def test_simple_password(self) -> None:
        """
        Test to verify that an API does not work with simple passwords.
        """

        data = {
            'username': 'test',
            'email': 'good_email@gmail.com',
            'password': '123',
        }

        response = self.client.post(self.path, data=data)

        self.assertEqual(response.status_code, 400)


class RevertCreateTestCase(APITestCase):
    client_class = tests_utils.LoggerAPIClient
    path = reverse('revert')

    def tearDown(self) -> None:
        utils.email.revert_queue.flush()

    def test_all_ok(self) -> None:
        """
        Test to verify that an API works with correct data.
        """

        models.User(username='test', email='good_email@gmail.com', is_verified=True).save()

        data = {'email': 'good_email@gmail.com'}

        response = self.client.post(self.path, data=data)

        self.assertEqual(response.status_code, 201)

        record = utils.email.revert_queue.find(data['email'])

        self.assertTrue(bool(record))

    def test_not_verified_email(self) -> None:
        """
        Test to verify that an API does not work with not verified email.
        """

        models.User(username='test', email='not_verified_email@gmail.com').save()

        data = {
            'email': 'not_verified_email@gmail.com',
        }

        response = self.client.post(self.path, data=data)

        self.assertEqual(response.status_code, 404)

    def test_nonexistent_email(self) -> None:
        data = {
            'email': 'nonexistent_email@gmail.com',
        }

        response = self.client.post(self.path, data=data)

        self.assertEqual(response.status_code, 404)


class RevertCompleteCreateTestCase(APITestCase):
    client_class = tests_utils.LoggerAPIClient
    path = reverse('revert-complete')

    def setUp(self) -> None:
        email = 'good_email@gmail.com'

        models.User(username='test', email=email, is_verified=True).save()

        utils.email.revert_queue.add(email)

        self._code: str = utils.email.revert_queue.find(email)['code']

    def tearDown(self) -> None:
        utils.email.revert_queue.flush()

    def test_all_ok(self) -> None:
        """
        Test to verify that an API works with correct data.
        """

        data = {'email': 'good_email@gmail.com', 'code': self._code, 'new_password': '123456789good_password$'}

        response = self.client.post(self.path, data=data)

        self.assertEqual(response.status_code, 201)

        content = json.loads(response.content)
        self.assertTrue(content.get('auth_token') is not None)

    def test_invalid_email(self) -> None:
        """
        Test to verify that an API does not work with invalid emails.
        """

        data = {'email': 'invalid_email', 'code': self._code, 'new_password': '123456789good_password$'}

        response = self.client.post(self.path, data=data)

        self.assertEqual(response.status_code, 400)

    def test_invalid_code(self) -> None:
        """
        Test to verify that an API does not work with invalid codes.
        """

        invalid_code: str = email_utils.EmailService.generate_code()

        while invalid_code == self._code:
            invalid_code = email_utils.EmailService.generate_code()

        data = {'email': 'good_email@gmail.com', 'code': invalid_code, 'new_password': '123456789good_password$'}

        response = self.client.post(self.path, data=data)

        self.assertEqual(response.status_code, 400)
