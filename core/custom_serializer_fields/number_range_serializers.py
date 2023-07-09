from rest_framework import serializers


class DecimalRangeFieldSerializer(serializers.Field):
    def to_representation(self, value):
        data = {
            "lower": value.lower,
            "upper": value.upper
        }
        return data
