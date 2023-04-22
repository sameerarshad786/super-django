from django.db import models

from core.models.user_model import User
from core.mixins import UUID


def store_files_path(instance, filename):
    return f"stores/{instance.id}/{filename}"


class StoreTypes(UUID):
    type = models.CharField(max_length=150, unique=True)
    valid_name = models.BooleanField(default=False)


class Stores(UUID):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=155, unique=True)
    store_type = models.ForeignKey(
        StoreTypes, models.SET_NULL, blank=True, null=True)
    images = models.FileField(
        upload_to=store_files_path, default="default.png")
    is_verified = models.BooleanField(default=False)
    location = models.JSONField(blank=True, null=True)

    def get_image(self):
        return True if self.images else False
