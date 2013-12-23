Django Access Manager
=====================

An abstract access manager for Django.

![Build Status](https://travis-ci.org/FundedByMe/django-access-manager.png)

A tidy and extendable way of specifying access requirements for views
instead of defining all the logic inside of the views or using mixins
for every requirement.

Installation
------------

Install using pip:

```
pip install django-access-manager
```

Or latest version in repo:

```
pip install -e git+https://github.com/FundedByMe/django-access-manager/#egg=access_manager
```

Add `'access_manager'` to your installed apps:

```python
INSTALLED_APPS += ('access_manager', )
```

Usage
-----

Extend your views with `ManagedAccessViewMixin` and specify view requirements:

```python
from access_manager.views import ManagedAccessViewMixin
from access_manager.requirements import Active, LoggedIn


class MyView(ManagedAccessViewMixin):
    access_requirements = [LoggedIn, Active]
    
    # … view code
```

Custom Requirements
-------------------

Easily specify your own requirements (in a local app or file) by extending the `Requirement` class:

```python
from access_manager.requirements import BaseRedirectRequirement


class LoggedIn(BaseExplainedRedirectRequirement):
    url_name = 'my_login_page'

    def is_fulfilled(self):
        return (self.request.user.is_authenticated() and
                self.request.user.is_active)
```

Advanced Usage
--------------

Require a profile field to be `True`:

```python
from access_manager.requirements import BaseRedirectRequirement


class BaseProfileFieldRequirement(BaseRedirectRequirement):
    profile_field_name = None

    def __init__(self, *args, **kwargs):
        self.required_field_value = kwargs.pop('required_field_value', True)
        super(BaseProfileFieldRequirement, self).__init__(*args, **kwargs)

    def is_fulfilled(self):
        if self.profile_field_name is None:
            raise ImproperlyConfigured(
                "ProfileFieldRequirements need to specify "
                "`profile_field_name`.")
        value = getattr(self.request.user.profile, self.profile_field_name)
        return value == self.required_field_value


class AcceptedTerms(BaseProfileFieldRequirement):
    url_name = 'accept_tos'
    profile_field_name = 'accepted_terms'


class ConfirmedEmail(BaseProfileFieldRequirement):
    url_name = 'prompt_email'
    profile_field_name = 'confirmed_email'

# … in your views.py:

from access_manager.views import ManagedAccessViewMixin


class MyView(ManagedAccessViewMixin, View):
    access_requirements = [AcceptedTerms, ConfirmedEmail]
    
    # … view code
 
```
