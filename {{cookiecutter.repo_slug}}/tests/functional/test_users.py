import pytest
from django.contrib.auth import get_user_model
from django.urls.base import reverse
from rest_framework.authtoken.models import Token

User = get_user_model()


class TestSignIn:

    @pytest.mark.django_db
    def test_success(self, faker, api_client, existed_user):
        test_data = {
            'email': existed_user.email,
            'password': 'password',
        }
        response = api_client.post(reverse('api:sign-in'), test_data)
        assert response.status_code == 200
        test_token = Token.objects.get(user=existed_user).key
        assert response.data['token'] == test_token

    @pytest.mark.django_db
    def test_failed(self, faker, api_client):
        test_data = {
            'email': faker.email(),
            'password': faker.password(),
        }
        response = api_client.post(reverse('api:sign-in'), test_data)
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_wrong_password(self, api_client, existed_user):
        test_data = {
            'email': existed_user.email,
            'password': 'password1',
        }
        response = api_client.post(reverse('api:sign-in'), test_data)
        assert response.status_code == 401


class TestSignout:

    @pytest.mark.django_db
    def test_success(self, user_client, existed_user):
        response = user_client.post(reverse('api:sign-out'), {})
        assert response.status_code == 202
        assert not Token.objects.filter(user=existed_user).exists()

    @pytest.mark.django_db
    def test_failed(self, api_client):
        response = api_client.post(reverse('api:sign-out'), {})
        assert response.status_code == 401


class TestPasswordChange:

    @pytest.mark.django_db
    def test_success_change(self, user_client, existed_user):
        new_password = 'new_password_123'
        response = user_client.post(
            reverse('api:password-change'),
            {
                'old_password': 'password',
                'new_password': new_password,
            }
        )
        assert response.status_code == 202
        existed_user.refresh_from_db()
        assert existed_user.check_password(new_password)

    @pytest.mark.django_db
    def test_wrong_old_password(self, user_client, existed_user):
        new_password = 'new_password_123'
        response = user_client.post(
            reverse('api:password-change'),
            {
                'old_password': 'wrong_password',
                'new_password': new_password,
            }
        )
        assert response.status_code == 400
        existed_user.refresh_from_db()
        assert existed_user.check_password('password')

    @pytest.mark.django_db
    def test_not_authorized(self, faker, api_client):
        response = api_client.post(
            reverse('api:password-change'),
            {
                'old_password': faker.password(),
                'new_password': faker.password(),
            }
        )
        assert response.status_code == 401
