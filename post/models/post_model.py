from django.db import models

from core.mixins import UUID
from core.models.user_model import User


def post_uploaded_files(instance, filename):
    """user uploaded pictures, videos, and documents"""
    return f"post_files/{instance.id}/{filename}"


class Post(UUID):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=50
    )
    text = models.TextField()
    other_files = models.FileField(
        upload_to=post_uploaded_files
    )

    def __str__(self) -> str:
        return f"{self.user}"
