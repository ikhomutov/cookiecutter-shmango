import environ

ROOT_DIR = environ.Path(__file__) - 3
PROJECT_DIR = ROOT_DIR.path('{{ cookiecutter.project_slug }}')
APPS_DIR = PROJECT_DIR.path('apps')

env = environ.Env()

READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=True)
if READ_DOT_ENV_FILE:
    env.read_env(str(ROOT_DIR.path('app.env')))

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', False)
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = env.bool('DJANGO_USE_TZ', default=True)
SECRET_KEY = env.str('DJANGO_SECRET_KEY', default='not-so-secret')
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[])

# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {
    'default': env.db('DATABASE_URL', default='sqlite:///db.sqlite3'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True
DATABASES['default']['CONN_MAX_AGE'] = env.int('CONN_MAX_AGE', default=60)

# URLS
# ------------------------------------------------------------------------------
ROOT_URLCONF = '{{ cookiecutter.project_slug }}.urls'
WSGI_APPLICATION = '{{ cookiecutter.project_slug }}.wsgi.application'

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
]
THIRD_PARTY_APPS = [
    {%- if cookiecutter.use_rest_framework != 'n' %}
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    {%- endif %}
]
LOCAL_APPS = [
    {%- if cookiecutter.custom_user_model != 'n' %}
    '{{ cookiecutter.project_slug }}.apps.users.apps.UsersConfig',
    {%- endif %}
    {%- if cookiecutter.use_rest_framework != 'n' %}
    '{{ cookiecutter.project_slug }}.apps.api.apps.ApiConfig',
    {%- endif %}
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# AUTHENTICATION
# ------------------------------------------------------------------------------
{%- if cookiecutter.custom_user_model != 'n' %}
AUTH_USER_MODEL = 'users.User'
{%- endif %}
LOGIN_URL = '/accounts/signin/'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'UserAttributeSimilarityValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'MinimumLengthValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'CommonPasswordValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'NumericPasswordValidator'),
    },
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    {%- if cookiecutter.use_rest_framework != 'n' %}
    'corsheaders.middleware.CorsMiddleware',
    {%- endif %}
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# STATIC
# ------------------------------------------------------------------------------
STATIC_ROOT = str(ROOT_DIR('staticfiles'))
STATIC_URL = '/static/'
STATICFILES_DIRS = []

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
STATICFILES_STORAGE = 'whitenoise.storage.ManifestStaticFilesStorage'

# MEDIA
# ------------------------------------------------------------------------------
MEDIA_ROOT = str(PROJECT_DIR('media'))
MEDIA_URL = '/media/'

# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# EMAIL
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env(
    'DJANGO_EMAIL_BACKEND',
    default='django.core.mail.backends.console.EmailBackend'
)
DEFAULT_FROM_EMAIL = env(
    'DJANGO_DEFAULT_FROM_EMAIL', default='Example <noreply@example.com>'
)
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)
EMAIL_SUBJECT_PREFIX = env('DJANGO_EMAIL_SUBJECT_PREFIX', default='[Example]')

# ADMIN
# ------------------------------------------------------------------------------
ADMIN_URL = env('DJANGO_ADMIN_URL', default='admin/')
ADMINS = [
    ('{{ cookiecutter.author_name }}', '{{ cookiecutter.author_email }}'),
]
MANAGERS = ADMINS

# LOGGING
# ------------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console', 'mail_admins'],
            'propagate': True
        }
    }
}

{% if cookiecutter.use_celery != 'n' -%}
# CELERY
# ------------------------------------------------------------------------------
CELERY_BROKER_URL = env.str('CELERY_BROKER_URL', default='')
CELERY_RESULT_BACKEND = env.str('CELERY_RESULT_BACKEND', default='')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

{% endif -%}
{% if cookiecutter.use_rest_framework != 'n' -%}
# DJANGO REST FRAMEWORK
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}

# DJANGO CORS HEADERS
# ------------------------------------------------------------------------------
CORS_ORIGIN_WHITELIST = env.list('DJANGO_CORS_ORIGIN_WHITELIST', default=[])

{% endif -%}

# APP SPECIFIC SETTINGS
# ------------------------------------------------------------------------------
