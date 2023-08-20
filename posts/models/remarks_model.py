from django.db import models
from django.contrib.auth import get_user_model

from .posts_model import Posts
from .comments_model import Comments
from core.mixins import UUID


class Remarks(UUID):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comment = models.ForeignKey(
        Comments, on_delete=models.SET_NULL, blank=True, null=True
    )
    like = models.BooleanField(default=False)
    heart = models.BooleanField(default=False)
    funny = models.BooleanField(default=False)
    insightful = models.BooleanField(default=False)
    disappoint = models.BooleanField(default=False)
