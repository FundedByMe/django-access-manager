from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

import factory


class InActiveUserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: 'user{0}'.format(n))
    first_name = "Bill"
    last_name = "Murray"
    is_active = False
    is_superuser = False
    is_staff = False
    email = "anemail@example.com"
    password = make_password("password")


class UserFactory(InActiveUserFactory):
    is_active = True
