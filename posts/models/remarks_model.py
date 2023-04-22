from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .posts_model import Posts
from .comments_model import Comments
from core.mixins import UUID


class Remarks(UUID):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comment = models.ForeignKey(
        Comments, on_delete=models.SET_NULL, blank=True, null=True
    )

    class Popularity(models.TextChoices):
        LIKE = ("like", _("LIKE"))
        HEART = ("heart", _("HEART"))
        FUNNY = ("funny", _("FUNNY"))
        INSIGHTFUL = ("insightful", _("INSIGHTFUL"))
        DISAPPOINT = ("disappoint", _("DISAPPOINT"))
    popularity = models.CharField(max_length=11, choices=Popularity.choices)
