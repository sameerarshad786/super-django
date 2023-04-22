from django.db import models

from . import Stores
from core.mixins import UUID


def product_media_path(instance, filename):
    return f"products/{instance.id}/{filename}"


class ProductTypes(UUID):
    type = models.CharField(max_length=150, unique=True)
    valid_name = models.BooleanField(default=False)


class Products(UUID):
    product_name = models.CharField(max_length=155)
    description = models.TextField()
    images = models.FileField(
        upload_to=product_media_path, default="default.png")
    store = models.ForeignKey(Stores, on_delete=models.CASCADE)
    product_type = models.ForeignKey(
        ProductTypes, models.SET_NULL, blank=True, null=True)
