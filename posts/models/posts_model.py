from django.db import models
from django.contrib.auth import get_user_model

from core.mixins import UUID


def Posts_uploaded_files(instance, filename):
    """user uploaded pictures, videos, and documents"""
    return f"posts/{instance.id}/{filename}"


class Posts(UUID):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    files = models.FileField(blank=True, upload_to=Posts_uploaded_files)

    def get_text(self):
        return f"{self.text[:20]}..."

    def get_files(self):
        return bool(self.files)
