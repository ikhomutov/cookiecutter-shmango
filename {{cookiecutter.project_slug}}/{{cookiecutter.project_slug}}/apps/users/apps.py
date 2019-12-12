from django.apps import AppConfig


class UsersAppConfig(AppConfig):
    name = '{{ cookiecutter.project_slug }}.apps.users'
    verbose_name = 'Users'
