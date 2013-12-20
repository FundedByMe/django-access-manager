from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.http import Http404

from .http import Http307


class BaseRequirement(object):
    def setup(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

    def is_fulfilled(self):
        raise ImproperlyConfigured(
            "Requirements need to implement a `is_fulfilled` method.")

    def not_fulfilled(self):
        raise ImproperlyConfigured(
            "Requirements need to implement a `not_fulfilled` method.")


class BasePageNotFoundRequirement(BaseRequirement):
    def not_fulfilled(self):
        raise Http404()


class Staff(BasePageNotFoundRequirement):
    def is_fulfilled(self):
        return self.request.user.is_staff


class SuperUser(BasePageNotFoundRequirement):
    def is_fulfilled(self):
        return self.request.user.is_superuser


class Active(BasePageNotFoundRequirement):
    def is_fulfilled(self):
        return self.request.user.is_active


class BaseRedirectRequirement(BaseRequirement):
    url_name = None
    append_next = True

    def get_url_args(self):
        return []

    def get_url_name(self):
        if self.url_name is None:
            raise ImproperlyConfigured(
                "You need to specify `url_name` or override the `get_url_name` "
                "method.")
        return self.url_name

    def get_url(self):
        url = reverse(self.get_url_name(), args=self.get_url_args())
        if self.append_next:
            url += "?next=%s" % self.request.get_full_path()
        return url

    def not_fulfilled(self):
        return Http307(self.get_url())


class LoggedIn(BaseRedirectRequirement):
    url_name = 'login'

    def is_fulfilled(self):
        return self.request.user.is_authenticated()
