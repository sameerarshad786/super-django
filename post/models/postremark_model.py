from django.db import models
from django.utils.translation import gettext_lazy as _

from core.mixins import UUID
from core.models.user_model import User
from .post_model import Post


class PostRemark(UUID):
    class Popularity(models.TextChoices):
        LIKE = ("like", _("LIKE"))
        DISLIKE = ("dislike", _("DISLIKE"))

    popularity = models.CharField(
        max_length=11, choices=Popularity.choices, blank=True
    )
    on_post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.user}"

    def get_on_postID(self):
        return f"{(self.on_post).id}"
