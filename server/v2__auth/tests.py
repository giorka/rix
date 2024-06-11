from __future__ import annotations

import logging
from typing import Any

from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APITestCase

from . import models


def logging_decorator(target: callable) -> callable:
    def wrapper(*args, **kwargs) -> Any:
        response = target(*args, **kwargs)

        logging.debug(str(response.content, 'UTF-8'))

        return response

    return wrapper


class ClientMixin:
    @logging_decorator
    def post(self: PathBasedAPITestCase, data: dict) -> Response:
        return self.client.post(self.path, data=data)


class PathBasedAPITestCase(APITestCase):
    path = 'example/url/'


class UserCreateAPIViewTestCase(PathBasedAPITestCase, ClientMixin):
    path = reverse('register')

    def test_all_ok(self) -> None:
        data = {
            'username': 'test',  # good username
            'email': 'good_email@gmail.com',  # good email
            'password': '123456789good_password$',  # good password
        }

        response = self.post(data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(models.User.objects.filter(username=data['username'], email=data['email']).exists())

    def test_taken_username(self) -> None:
        """
        Test to verify that an API does not work with taken usernames.
        """

        models.User(username='taken_username').save()

        data = {
            'username': 'taken_username',  # bad username
            'email': 'good_email@gmail.com',  # good email
            'password': '123456789good_password$',  # good password
        }

        response = self.post(data)

        self.assertEqual(response.status_code, 400)

    def test_invalid_email(self) -> None:
        """
        Test to verify that an API does not work with invalid emails.
        """

        data = {
            'username': 'test',  # good username
            'email': 'invalid_email',  # bad email
            'password': '123456789good_password$',  # good password
        }

        response = self.post(data)

        self.assertEqual(response.status_code, 400)

    def test_simple_password(self) -> None:
        """
        Test to verify that an API does not work with simple passwords.
        """

        data = {
            'username': 'test',  # good username
            'email': 'good_email@gmail.com',  # good email
            'password': '123',  # bad password
        }

        response = self.post(data)

        self.assertEqual(response.status_code, 400)


#     def test_revert(self) -> None:
#         data = {
#             'username': 'test',
#             'email': 'test@test.com',
#         }
#
#         user = models.User(**data)
#         user.set_password(raw_password='12345678a$')
#         user.is_verified = True
#         user.save()
#
#         document = {'email': data['email']}
#
#         response = self.client.post(reverse('revert'), data=document)
#
#         self.assertTrue(response.status_code in revert_good_status_codes, msg='Revert Request Failed')
#
#         code = utils.email.revert_queue.find({'email': data['email']})['code']
#         new_password = '987654321$'
#         document |= {'code': code, 'new_password': new_password}
#
#         response = self.client.post(reverse('revert-complete'), data=document)
#
#         self.assertTrue(response.status_code in revert_good_status_codes, msg='Revert Confirmation Request Failed')
#
#         user = get_object_or_404(models.User, email=data['email'], is_verified=True)
#         is_password_set = user.check_password(new_password)
#
#         self.assertTrue(is_password_set, msg='Error Setting Password')
