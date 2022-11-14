from django.db import models
from django.contrib.auth import get_user_model

from core.mixins import UUID


def feeds_uploaded_files(instance, filename):
    """user uploaded pictures, videos, and documents"""
    return f"feeds/{instance.id}/{filename}"


class Feeds(UUID):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()
    files = models.FileField(upload_to=feeds_uploaded_files)

    def get_text(self):
        return f"{self.text[:20]}..."

    def get_files(self):
        return bool(self.files)
