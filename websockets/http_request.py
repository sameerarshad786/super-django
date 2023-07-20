import os

from django.http import HttpRequest


class Request(HttpRequest):
    def _get_raw_host(self):
        self.META["SERVER_NAME"] = os.getenv("SERVER_NAME")
        self.META["SERVER_PORT"] = os.getenv("SERVER_PORT")
        if self.META["SERVER_PORT"]:
            host = "%s:%s" % (self.META["SERVER_NAME"], self.META["SERVER_PORT"])
        else:
            host = "%s" % (self.META["SERVER_NAME"])
        return host
