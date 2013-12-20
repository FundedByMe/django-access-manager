"""
Use 303 and 307 instead of 302, to deal with faulty browser implementations. See
http://stackoverflow.com/questions/4764297/difference-between-http-redirect-codes
for more on the issue.

"""

from django.http import HttpResponseRedirect


class Http303(HttpResponseRedirect):
    status_code = 303


class Http307(HttpResponseRedirect):
    status_code = 307
