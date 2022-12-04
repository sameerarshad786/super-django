from django.db import models

from core.models.user_model import User
from core.mixins import UUID


def store_files_path(instance, filename):
    return f"stores/{instance.id}/{filename}"


class Types(UUID):
    type = models.CharField(max_length=150, unique=True)
    valid_name = models.BooleanField(default=False)


class Store(UUID):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=155, unique=True)
    store_type = models.CharField(max_length=100)
    type = models.ForeignKey(Types, models.SET_NULL, blank=True, null=True)
    image = models.FileField(upload_to=store_files_path, default="default.png")
    is_verified = models.BooleanField(default=False)
    location = models.JSONField(blank=True)

    def get_image(self):
        return bool(self.image)
