import factory
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.DjangoModelFactory):
    email = factory.Faker('email')
    is_active = True
    is_staff = False

    class Meta:
        model = User
