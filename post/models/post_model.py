from django.db import models

from core.models.user_model import User
from core.mixins import UUID


def post_uploaded_files(instance, filename):
    """user uploaded pictures, videos, and documents"""
    return f"post_files/{instance.id}/{filename}"


class Post(UUID):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    files = models.FileField("file", upload_to=post_uploaded_files)

    class Meta:
        ordering = ("-created_at", )
