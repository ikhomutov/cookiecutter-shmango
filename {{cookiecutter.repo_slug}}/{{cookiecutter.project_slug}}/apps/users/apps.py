from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = '{{ cookiecutter.project_slug }}.apps.users'
    verbose_name = 'Users'
