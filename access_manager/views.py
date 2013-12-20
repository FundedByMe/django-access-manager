from django.core.exceptions import ImproperlyConfigured

from .requirements import BaseRequirement


class ManagedAccessViewMixin(object):
    """
    Runs checks for requirements before running `dispatch` of the subclass.
    The subclass needs to specify `access_requirements` as an iterable of
    requirements.

    """

    access_requirements = None

    def get_access_requirements(self):
        if self.access_requirements is None:
            raise ImproperlyConfigured(
                "Views that extends ManagedAccessViewMixin need to specify "
                "`access_requirements` or implement a "
                "`get_access_requirements` method.")
        return self.access_requirements

    def dispatch(self, *args, **kwargs):
        klasses = self.get_access_requirements()

        for requirement in klasses:
            if not isinstance(requirement, BaseRequirement):
                requirement = requirement()
            requirement.setup(*args, **kwargs)
            if not requirement.is_fulfilled():
                return requirement.not_fulfilled()

        return super(ManagedAccessViewMixin, self).dispatch(*args, **kwargs)
