from os import environ

from celery import Celery

environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

application = Celery('global')
application.config_from_object('django.conf:settings', namespace='CELERY')
application.autodiscover_tasks()
