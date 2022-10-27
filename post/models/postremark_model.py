from django.db import models
from django.utils.translation import gettext_lazy as _
from pak_social.settings import WEBSITE_URL

from core.models.user_model import User
from core.mixins import UUID
from post.models.post_model import Post


def comment_media_path(instance, filename):
    return f"comments/{instance.id}/{filename}"


class PostRemark(UUID):
    class Popularity(models.TextChoices):
        LIKE = ("like", _("LIKE"))
        DISLIKE = ("dislike", _("DISLIKE"))

    popularity = models.CharField(max_length=11, choices=Popularity.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    on_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True
    )


class Comments(UUID):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    on_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True
    )
    comment = models.TextField(blank=True)
    files = models.FileField("file", upload_to=comment_media_path, blank=True)

    def get_replies(self):
        result = []
        for comment in Comments.objects.filter(parent=self):
            result.append({
                "id": comment.id,
                "user_id": comment.user.id,
                "user_email": comment.user.email,
                "username": comment.user.profile.username,
                "profile_image": WEBSITE_URL + str(
                    comment.user.profile.profile_image.url
                ) if comment.user.profile.profile_image else None,
                "on_post": comment.on_post.id,
                "comment": comment.comment,
                "files": WEBSITE_URL + str(
                    comment.files.url
                ) if comment.files else None,
                "created": comment.created(),
                "updated": comment.updated(),
                "child": Comments.get_replies(comment)
            })
            return result
