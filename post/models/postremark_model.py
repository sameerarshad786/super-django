from django.db import models
from django.utils.translation import gettext_lazy as _

from core.mixins import UUID
from core.models.user_model import User
from .post_model import Post


def comment_media_path(instance, filename):
    return f"comments/{instance.id}/{filename}"


class PostRemark(UUID):
    class Popularity(models.TextChoices):
        LIKE = ("like", _("LIKE"))
        DISLIKE = ("dislike", _("DISLIKE"))

    popularity = models.CharField(max_length=11, choices=Popularity.choices)
    on_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comments(UUID):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    on_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    files = models.FileField(upload_to=comment_media_path, blank=True)
