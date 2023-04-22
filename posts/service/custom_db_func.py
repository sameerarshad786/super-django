from django.db.models import Aggregate
from django.db import models


class CustomBoolOr(Aggregate):
    function = 'BOOL_OR'
    output_field = models.BooleanField()

    def convert_value(self, value, expression, connection):
        return True if value else False
