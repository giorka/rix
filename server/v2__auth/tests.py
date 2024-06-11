from __future__ import annotations

from django.test import TestCase
from rest_framework.reverse import reverse
from v2.utils import get_object_or_404

from . import models
from . import utils

register_tests_map = [
    (
        201,
        {
            'data': {'username': 'test', 'email': 'test@test.com'},
            'create_data': {'password': '12345678a$'},
        },
    ),
    (
        400,
        {
            'data': {'username': 'test', 'email': 'test'},
            'create_data': {'password': '12345678a$'},
        },
    ),
    (
        400,
        {
            'data': {'username': 'test', 'email': 'test@test.com'},
            'create_data': {'password': '123'},
        },
    ),
]
register_good_status_codes = (201,)

revert_good_status_codes = (201,)


class AuthTestCase(TestCase):
    def test_register(self) -> None:
        for status_code, details in register_tests_map:
            response = self.client.post(reverse('register'), data=details['data'] | details['create_data'])

            self.assertEqual(status_code, response.status_code, msg='Status Code Does Not Match Expected')

            is_exists = models.User.objects.filter(**details['data']).exists()

            self.assertEqual(is_exists, status_code in register_good_status_codes)

            models.User.objects.all().delete()

    def test_revert(self) -> None:
        data = {
            'username': 'test',
            'email': 'test@test.com',
        }

        user = models.User(**data)
        user.set_password(raw_password='12345678a$')
        user.is_verified = True
        user.save()

        document = {'email': data['email']}

        response = self.client.post(reverse('revert'), data=document)

        self.assertTrue(response.status_code in revert_good_status_codes, msg='Revert Request Failed')

        code = utils.email.revert_queue.find({'email': data['email']})['code']
        new_password = '987654321$'
        document |= {'code': code, 'new_password': new_password}

        response = self.client.post(reverse('revert-complete'), data=document)

        self.assertTrue(response.status_code in revert_good_status_codes, msg='Revert Confirmation Request Failed')

        user = get_object_or_404(models.User, email=data['email'], is_verified=True)
        is_password_set = user.check_password(new_password)

        self.assertTrue(is_password_set, msg='Error Setting Password')
