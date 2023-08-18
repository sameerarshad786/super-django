from django.contrib.gis.geos import Point
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from psycopg2.extras import NumericRange

from rest_framework import serializers
from rest_framework.utils.formatting import lazy_format

from .service import get_countries


class DecimalRangeFieldSerializer(serializers.DictField):
    default_error_messages = {
        'invalid': _('Not a valid nuimber.'),
        'blank': _('This field may not be blank.'),
        'lower': _('lower field may not be blank.'),
        'min_value': _('Ensure this field has at least {min_value}.'),
        'max_value': _('Ensure this field has value more than {max_value}.'),
    }

    def __init__(self, **kwargs):
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
        lower = data.get("lower")
        upper = data.get("upper")
        if not lower:
            return self.fail('lower')
        return NumericRange(float(lower), float(upper) if upper else None, '(]')

    def to_representation(self, value):
        data = {
            "lower": value.lower,
            "upper": value.upper
        }
        return data


class PointSerializer(serializers.DictField):
    default_error_messages = {
        'blank': _('This field may not be blank.'),
        'longitude': _('longitude field may not be blank.'),
        'latitude': _('latitude field may not be blank.')
    }

    def to_internal_value(self, data):
        longitude = data.get("longitude")
        latitude = data.get("latitude")
        altitude = data.get("altitude", 0)
        if longitude is None:
            return self.fail('longitude')
        if latitude is None:
            return self.fail('latitude')
        return Point((float(longitude), float(latitude)), float(altitude))

    def to_representation(self, value):
        longitude = value.x
        latitude = value.y

        data = get_countries(longitude, latitude)
        _data = {
            "longitude": value.x,
            "latitude": value.y,
            "altitude": value.z,
            "data": data
        }
        return _data
