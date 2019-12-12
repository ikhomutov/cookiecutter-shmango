import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{ cookiecutter.project_slug }}.settings.dev')

app = Celery('{{ cookiecutter.project_slug }}')

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'Example task': {
        'task': 'example_task',
        'schedule': timedelta(minutes=5),
        'options': {
            'expires': 60 * 60,
        }
    },
}
