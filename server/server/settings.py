from __future__ import annotations

from json import loads
from os import getenv
from os import path
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG: str | None = getenv(key='DEBUG')

if not DEBUG:
    load_dotenv()  # loads .env file
    DEBUG: str | None = getenv(key='DEBUG')

DEBUG: bool = loads(DEBUG)

SECRET_KEY = getenv(key='SECRET_KEY')

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
    'v1',
    'v1__auth',
    'v1__users',
)

INSTALLED_APPS = [
    *DJANGO_APPS,
    *APPS,
    'rest_framework',
    'djoser',
    'rest_framework.authtoken',
]

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

AUTH_USER_MODEL = 'v1__auth.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}

DATABASES = {  # pip install psycopg2
    'default': {
        'ENGINE': 'django.db.backends.' + getenv(key='DB_ENGINE'),
        'NAME': getenv(key='DB_NAME'),
        'USER': getenv(key='DB_USER'),
        'PASSWORD': getenv(key='DB_PASSWORD'),
        'HOST': getenv(key='DB_HOST'),
        'PORT': getenv(key='DB_PORT'),
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
    EMAIL_HOST = getenv(key='EMAIL_HOST')
    EMAIL_PORT = getenv(key='EMAIL_PORT')
    EMAIL_USE_SSL = loads(getenv(key='EMAIL_USE_SSL'))

    EMAIL_HOST_USER = getenv(key='EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = getenv(key='EMAIL_HOST_PASSWORD')

    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
    SERVER_EMAIL = EMAIL_HOST_USER
    EMAIL_ADMIN = EMAIL_HOST_USER

MONGO_PORT = 27017
MONGO_HOST = f'mongodb://{getenv(key="MONGO_HOST")}:' + str(MONGO_PORT) + '/'
MONGO_KEY = getenv(key='MONGO_KEY')

CELERY_BROKER_URL = 'redis://localhost:6379/0'

MEDIA_URL: str = '/storage/'
MEDIA_ROOT: str = path.join(BASE_DIR, 'storage')

MAX_USER_MEMORY: int = 536_870_912  # NOTE: Записано в байтах
MAX_PREMIUM_USER_MEMORY: int = 1_073_741_824  # NOTE: Записано в байтах

MAX_USER_FILES_COUNT: int = 25
MAX_PREMIUM_USER_FILES_COUNT: int = 40

ERRORS: dict[str, str] = dict(
    INCORRECT_CODE='Некорректный код.',
    NO_ATTEMPT='Попытки закончились.',
    NO_REGISTRATION_DETAILS='Регистрационные данные не найдены.',
    NO_MEMORY='Превышено максимальное количество выделенной памяти для пользователя.',
    NO_FILES_SLOTS='Превышено максимальное количество файлов для пользователя.',

)
