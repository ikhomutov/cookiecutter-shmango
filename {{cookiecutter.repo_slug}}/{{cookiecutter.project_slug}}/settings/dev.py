from .base import *  # noqa

# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# whitenoise
# ------------------------------------------------------------------------------
INSTALLED_APPS.insert(0, 'whitenoise.runserver_nostatic')  # noqa F405
