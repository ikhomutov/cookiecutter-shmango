import pytest

pytestmark = pytest.mark.django_db


class TestUserManagers:

    def test_create_user(self, django_user_model, faker):
        email = faker.email()
        password = faker.password()
        user = django_user_model.objects.create_user(email, password)
        assert user.email == email
        assert user.check_password(password)

    def test_create_user_empty_password(self, django_user_model, faker):
        email = faker.email()
        user = django_user_model.objects.create_user(email)
        assert user.email == email
        assert not user.has_usable_password()

    def test_create_user_raises_error_on_empty_email(self, django_user_model):
        with pytest.raises(ValueError):
            django_user_model.objects.create_user(email='')

    def test_create_superuser(self, django_user_model, faker):
        email = faker.email()
        password = faker.password()
        user = django_user_model.objects.create_superuser(email, password)
        assert user.email == email
        assert user.check_password(password)
        assert user.is_superuser
        assert user.is_staff

    def test_create_superuser_raises_error_on_false_is_superuser(
        self, django_user_model, faker
    ):
        with pytest.raises(ValueError):
            django_user_model.objects.create_superuser(
                email=faker.email(),
                password=faker.password(),
                is_superuser=False,
            )

    def test_create_superuser_raises_error_on_false_is_staff(
        self, django_user_model, faker
    ):
        with pytest.raises(ValueError):
            django_user_model.objects.create_superuser(
                email=faker.email(),
                password=faker.password(),
                is_staff=False,
            )
