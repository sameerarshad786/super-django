from django.db import models

from core.models.core_model import UUID
from core.models.user_model import User


"""user uploaded pictures, videos, and documents"""
def post_uploaded_files(instance, filename):
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
