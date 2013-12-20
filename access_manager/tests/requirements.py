from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth.models import AnonymousUser

from access_manager.requirements import (
    Staff, SuperUser, LoggedIn, Active)
from .factories import UserFactory, InActiveUserFactory


class TestRequirements(TestCase):
    request = None

    def setUp(self):
        self.request = None

    def set_request(self, **kwargs):
        self.request = HttpRequest()
        for k, v in kwargs.items():
            setattr(self.request, k, v)

    def assert_requirement_fulfilled(self, requirement):
        requirement.setup(self.request)
        self.assertTrue(
            requirement.is_fulfilled(), msg="The requirement is not fulfilled")

    def assert_requirement_unfulfilled(self, requirement):
        requirement.setup(self.request)
        self.assertFalse(
            requirement.is_fulfilled(), msg="The requirement is fulfilled")

    def test_staff(self):
        user = UserFactory.build(is_staff=False)
        self.set_request(user=user)
        self.assert_requirement_unfulfilled(Staff())

        user.is_staff = True
        self.assert_requirement_fulfilled(Staff())

    def test_superuser(self):
        user = UserFactory.build(is_superuser=False)
        self.set_request(user=user)
        self.assert_requirement_unfulfilled(SuperUser())

        user.is_superuser = True
        self.assert_requirement_fulfilled(SuperUser())

    def test_active(self):
        user = InActiveUserFactory.build()
        self.set_request(user=user)
        self.assert_requirement_unfulfilled(Active())

        user.is_active = True
        self.assert_requirement_fulfilled(Active())

    def test_logged_in(self):
        self.set_request(user=AnonymousUser())
        self.assert_requirement_unfulfilled(LoggedIn())

        self.set_request(user=UserFactory.build())
        self.assert_requirement_fulfilled(LoggedIn())
