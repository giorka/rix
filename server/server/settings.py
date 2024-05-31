from __future__ import annotations

import logging
from json import loads
from os import getenv
from os import path
from pathlib import Path
from sys import argv

from boto3 import client
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG: str | None = getenv('DEBUG')

if not DEBUG:
    load_dotenv()  # loads .env file
    DEBUG: str | None = getenv('DEBUG')

DEBUG: bool = loads(DEBUG)

SECRET_KEY = getenv('SECRET_KEY')

ALLOWED_HOSTS = [
    '127.0.0.1',
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_imap_backend',
]

APPS = (
    'v2',
    'v2__files',
    'v2__auth',
)

INSTALLED_APPS = (
    *DJANGO_APPS,
    *APPS,
    'rest_framework',
    'djoser',
    'rest_framework.authtoken',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'server.wsgi.application'

AUTH_USER_MODEL: str = 'v2__auth.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}

DATABASES = {  # pip install psycopg2
    'default': {
        'ENGINE': 'django.db.backends.' + getenv('DB_ENGINE'),
        'NAME': getenv('DB_NAME'),
        'USER': getenv('DB_USER'),
        'PASSWORD': getenv('DB_PASSWORD'),
        'HOST': getenv('DB_HOST'),
        'PORT': getenv('DB_PORT'),
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

if not DEBUG:
    EMAIL_HOST = getenv('EMAIL_HOST')
    EMAIL_PORT = getenv('EMAIL_PORT')
    EMAIL_USE_SSL = loads(getenv('EMAIL_USE_SSL'))

    EMAIL_HOST_USER = getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = getenv('EMAIL_HOST_PASSWORD')

    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
    SERVER_EMAIL = EMAIL_HOST_USER
    EMAIL_ADMIN = EMAIL_HOST_USER

MONGO_PORT = 27017
MONGO_HOST = f'mongodb://{getenv("MONGO_HOST")}:' + str(MONGO_PORT) + '/'
MONGO_KEY = getenv('MONGO_KEY')

CELERY_BROKER_URL = 'redis://localhost:6379/0'

MEDIA_URL: str = '/storage/'
MEDIA_ROOT: str = path.join(BASE_DIR, 'storage')

MAX_USER_MEMORY: int = 536_870_912  # NOTE: Записано в байтах
MAX_PREMIUM_USER_MEMORY: int = 1_073_741_824  # NOTE: Записано в байтах

MAX_USER_FILES: int = 25  # NOTE: Записано в единицах
MAX_PREMIUM_USER_FILES: int = 40  # NOTE: Записано в единицах

MAX_USER_DOMAIN: int = 2  # NOTE: Записано в единицах.

ERRORS: dict[str, str] = dict(
    NO_CORRECT_CODE='Некорректный код.',
    NO_ATTEMPT='Попытки закончились.',
    NO_REGISTRATION_DETAILS='Регистрационные данные не найдены.',
    NO_MEMORY='Превышено максимальное количество выделенной памяти для пользователя.',
    NO_FILES_SLOTS='Превышено максимальное количество файлов для пользователя.',
    NO_DOMAINS_SLOTS='Превышено максимальное количество файлов с доменным именем для пользователя.',

)

ERRORS_V2: dict[str, str] = dict(
    NO_CORRECT_CODE='Некорректный код.',
    NO_REGISTRATION_DETAILS='Регистрационные данные не найдены.',
    NO_VERIFY_POSSIBILITY='Аккаунт уже верифицирован.',
    NO_MEMORY='Превышено максимальное количество выделенной памяти для пользователя.',
    NO_FILES_SLOTS='Превышено максимальное количество файлов для пользователя.',
    NO_DOMAINS_SLOTS='Превышено максимальное количество файлов с доменным именем для пользователя.',
)

DJOSER = {
    'PASSWORD_VALIDATORS': ('django.contrib.auth.password_validation.validate_password',),
}

launch_argument: str = argv[1].lower()

if launch_argument == 'runserver':
    logging.debug('Connecting To Storage Server...')

    storage = client(
        service_name='s3',
        endpoint_url='https://' + getenv('AWS_ENDPOINT_URL'),
        aws_access_key_id=getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=getenv('AWS_SECRET_ACCESS_KEY'),
    )

    AWS_BUCKET = getenv('AWS_BUCKET')
else:
    logging.debug(
        f'Storage Server Connection Canceled!\nBecause Of {launch_argument=}',
    )

    storage = AWS_BUCKET = None
