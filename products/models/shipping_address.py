from django.contrib.gis.db import models

from phonenumber_field.modelfields import PhoneNumberField

from core.models import User
from core.mixins import UUID


class ShippingAddress(UUID):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country_code = models.CharField(max_length=3)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50, blank=True, null=True)
    street_address = models.CharField(max_length=255)
    postal_code = models.IntegerField()
    meta = models.JSONField(default=dict)
    phone_number = PhoneNumberField()
