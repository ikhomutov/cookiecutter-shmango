import pytest


@pytest.fixture()
def existed_user(db, django_user_model):
    User = django_user_model
    {%- if cookiecutter.custom_user_model == "n" %}
    username = 'test_user'
    {%- endif %}
    email = 'test@email.com'
    password = 'password'
    try:
        user = User.objects.get(
            {%- if cookiecutter.custom_user_model == "n" -%}
            username=username
            {%- else -%}
            email=email
            {%- endif -%}
        )
        user.set_password(password)
        user.save()
    except User.DoesNotExist:
        user = User.objects.create_user(
            {%- if cookiecutter.custom_user_model == "n" %}
            username=username,
            {%- endif %}
            email=email,
            password=password,
        )
    return user
{% if cookiecutter.use_rest_framework != 'n' %}

@pytest.fixture()
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture()
def user_client(db, api_client, existed_user):
    """A test client logged in as a user with proper auth header."""

    from rest_framework.authtoken.models import Token
    token, _ = Token.objects.get_or_create(user=existed_user)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return api_client
{% endif -%}
