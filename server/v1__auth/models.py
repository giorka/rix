from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models


class User(AbstractUser):
    first_name = last_name = None  # Удаляем поля
    cloud_size = models.IntegerField(
        default=0,
        validators=(
            validators.MaxValueValidator(10000000000),
        )
    )
