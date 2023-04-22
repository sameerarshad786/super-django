from django.db import models
from django.contrib.auth import get_user_model

from core.mixins import UUID
from .posts_model import Posts


def comment_media_path(instance, filename):
    return f"comments/{instance.id}/{filename}"


class Comments(UUID):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True
    )
    comment = models.TextField(blank=True)
    files = models.FileField(blank=True, upload_to=comment_media_path)

    def get_text(self):
        return f"{self.comment[:20]}"

    def get_files(self):
        return bool(self.files)
