from django.db import models
from django.contrib.auth import get_user_model

from core.mixins import UUID
from .feeds_model import Feeds


def comment_media_path(instance, filename):
    return f"comments/{instance.id}/{filename}"


class Comments(UUID):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    on_post = models.ForeignKey(Feeds, on_delete=models.CASCADE)
    on_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True
    )
    text = models.TextField()
    files = models.FileField(upload_to=comment_media_path)

    def get_text(self):
        return f"{self.text[:20]}"

    def get_files(self):
        return bool(self.files)
