import json

from psycopg2.extras import NumericRange

from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from rest_framework.serializers import Field
from rest_framework.utils.formatting import lazy_format


class DecimalRangeFieldSerializer(Field):
    default_error_messages = {
        'invalid': _('Not a valid nuimber.'),
        'blank': _('This field may not be blank.'),
        'lower': _('lower field may not be blank.'),
        'min_value': _('Ensure this field has at least {min_value}.'),
        'max_value': _('Ensure this field has value more than {max_value}.'),
    }

    def __init__(self, **kwargs):
        self.allow_blank = kwargs.pop('allow_blank', False)
        self.min_value = kwargs.pop('min_value', None)
        self.max_value = kwargs.pop('max_value', None)
        super().__init__(**kwargs)

        if self.min_value:
            message = lazy_format(self.error_messages['min_value'], min_value=self.min_value)
            self.validators.append(
                MinValueValidator(self.min_value, message=message))

        if self.min_value:
            message = lazy_format(self.error_messages['max_value'], max_value=self.max_value)
            self.validators.append(
                MaxValueValidator(self.max_value, message=message))

    def to_internal_value(self, data):
        if not data:
            return self.fail('blank')
        _data = json.loads(data)
        lower = _data.get("lower")
        upper = _data.get("upper")
        if not lower:
            return self.fail('lower')
        return NumericRange(float(lower), float(upper) if upper else None, '(]')

    def to_representation(self, value):
        data = {
            "lower": value.lower,
            "upper": value.upper
        }
        return data
