from os import getenv
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = getenv(key='SECRET_KEY')

DEBUG = {'true': True, 'false': False}.get(getenv(key='DEBUG'))

ALLOWED_HOSTS = []

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_imap_backend',
]

INSTALLED_APPS = [
    *DJANGO_APPS,
    'rest_framework',

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

DATABASES = {  # pip install psycopg2
    'default': {
        'ENGINE': 'django.db.backends.' + getenv(key='ENGINE'),
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = getenv(key='EMAIL_HOST')
# EMAIL_PORT = getenv(key='EMAIL_PORT')
# EMAIL_USE_SSL = {'true': True, 'false': False}.get(getenv(key='EMAIL_USE_SSL'))
#
# EMAIL_HOST_USER = getenv(key='EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = getenv(key='EMAIL_HOST_PASSWORD')
#
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# SERVER_EMAIL = EMAIL_HOST_USER
# EMAIL_ADMIN = EMAIL_HOST_USER

MONGO_PORT = 27017
MONGO_HOST = 'mongodb://localhost:' + str(MONGO_PORT) + '/'
MONGO_KEY = getenv(key='MONGO_KEY')

CELERY_BROKER_URL = 'redis://localhost:6379/0'
