import pytest


class TestUserModel:

    @pytest.mark.django_db
    def test_str(self, existed_user):
        assert str(existed_user) == existed_user.email
