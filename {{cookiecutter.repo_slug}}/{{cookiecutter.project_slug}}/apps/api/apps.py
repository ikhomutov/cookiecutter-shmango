from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = '{{ cookiecutter.project_slug }}.apps.api'
    verbose_name = 'API'
