from django.apps import AppConfig


class ApiAppConfig(AppConfig):
    name = '{{ cookiecutter.project_slug }}.apps.api'
    verbose_name = 'API'
