from django.test import TestCase

from access_manager.views import ManagedAccessViewMixin
from access_manager.requirements import BaseRequirement


class SuccessfulRequirement(BaseRequirement):
    not_fulfilled_called = False
    is_fulfilled_called = False
    return_value = True

    def not_fulfilled(self):
        self.not_fulfilled_called = True

    def is_fulfilled(self):
        self.is_fulfilled_called = True
        return self.return_value


class UnSuccessfulRequirement(SuccessfulRequirement):
    return_value = False


class View(object):
    dispatch_called = False

    def dispatch(self, *args, **kwargs):
        self.dispatch_called = True


class FakeView(ManagedAccessViewMixin, View):
    pass


class TestManagedAccessViewMixin(TestCase):
    def setUp(self):
        self.view = FakeView()
        self.request = {}

    def test_successful(self):
        first = SuccessfulRequirement()
        second = SuccessfulRequirement()
        self.view.access_requirements = [
            first, second]
        self.view.dispatch(self.request)
        self.assertTrue(self.view.dispatch_called)
        self.assertTrue(first.is_fulfilled_called)
        self.assertTrue(second.is_fulfilled_called)

    def test_first_unfulfilled(self):
        first = UnSuccessfulRequirement()
        second = SuccessfulRequirement()
        self.view.access_requirements = [first, second]
        self.view.dispatch(self.request)
        self.assertFalse(self.view.dispatch_called)
        self.assertTrue(first.is_fulfilled_called)
        self.assertTrue(first.not_fulfilled_called)
        self.assertFalse(second.is_fulfilled_called)
        self.assertFalse(second.not_fulfilled_called)

    def test_second_unfulfilled(self):
        first = SuccessfulRequirement()
        second = UnSuccessfulRequirement()
        self.view.access_requirements = [first, second]
        self.view.dispatch(self.request)
        self.assertFalse(self.view.dispatch_called)
        self.assertTrue(first.is_fulfilled_called)
        self.assertFalse(first.not_fulfilled_called)
        self.assertTrue(second.is_fulfilled_called)
        self.assertTrue(second.not_fulfilled_called)
