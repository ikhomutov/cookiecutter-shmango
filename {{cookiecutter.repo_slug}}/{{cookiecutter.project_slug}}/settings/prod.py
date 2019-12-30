import sentry_sdk
{% if cookiecutter.use_sentry == 'y' -%}
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
{%- endif %}

from .base import *  # noqa
from .base import env

# CACHES
# ------------------------------------------------------------------------------
{%- if cookiecutter.cache_backend == 'redis' %}
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': True,
        }
    }
}

{% elif cookiecutter.cache_backend == 'memcached' %}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': env('MEMCACHED_URL'),
    }
}

{% elif cookiecutter.cache_backend == 'db' %}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': env('DJANGO_CACHE_TABLE'),
    }
}

{% endif -%}

# SECURITY
# ------------------------------------------------------------------------------
SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)
SESSION_COOKIE_SECURE = env.bool('DJANGO_SESSION_COOKIE_SECURE', default=True)

# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[0]['OPTIONS']['loaders'] = [  # noqa F405
    (
        'django.template.loaders.cached.Loader',
        [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]
    ),
]

# GUNICORN
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['gunicorn']  # noqa F405

{% if cookiecutter.use_sentry == 'y' -%}
# SENTRY
# ------------------------------------------------------------------------------
SENTRY_DSN = env.str('SENTRY_DSN', default='')
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            CeleryIntegration(),
            DjangoIntegration(),
            LoggingIntegration(),
        ],
        environment=env.str('SENTRY_ENVIRONMENT'),
    )
{% endif -%}
