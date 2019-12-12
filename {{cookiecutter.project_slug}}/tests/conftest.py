import pytest


@pytest.fixture()
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture()
def existed_user(db, django_user_model):
    User = django_user_model
    try:
        user = User.objects.get(email='test@email.com')
        user.set_password('password')
        user.save()
    except User.DoesNotExist:
        user = User.objects.create_user(
            email='test@email.com',
            password='password',
        )
    return user


@pytest.fixture()
def user_client(db, api_client, existed_user):
    """A test client logged in as a user with proper auth header."""

    from rest_framework.authtoken.models import Token
    token, _ = Token.objects.get_or_create(user=existed_user)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return api_client
