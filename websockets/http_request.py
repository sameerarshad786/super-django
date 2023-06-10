import os

from django.http import HttpRequest
from django.urls import get_script_prefix


def request():
    request = HttpRequest()
    request.META["SERVER_NAME"] = os.getenv("SERVER_NAME")
    request.META["SERVER_PORT"] = os.getenv("SERVER_PORT")
    request.path_info = get_script_prefix()
    return request
