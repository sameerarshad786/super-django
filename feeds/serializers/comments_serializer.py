from rest_framework import serializers

from ..models import Comments, Remarks, Popularity
from ..service import get_replies


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = (
            "id", "user", "on_post", "on_comment", "text", "files", "created",
            "updated"
        )
        extra_kwargs = {
            "user": {"read_only": True},
            "text": {"required": False},
            "files": {"required": False}
        }

    def to_representation(self, instance):
        request = self.context["request"]
        popularity_details = []
        data = dict()

        # post remarks
        comment_remarks = Remarks.objects.filter(
            on_post=instance.on_post.id, on_comment=instance.id
        )
        current_user_action = comment_remarks.filter(
            user=request.user
        ).values("popularity")
        likes = comment_remarks.filter(popularity=Popularity.LIKE)
        hearts = comment_remarks.filter(popularity=Popularity.HEART)
        funny = comment_remarks.filter(popularity=Popularity.FUNNY)
        insightful = comment_remarks.filter(popularity=Popularity.INSIGHTFUL)
        disappoint = comment_remarks.filter(popularity=Popularity.DISAPPOINT)
        total_replies = Comments.objects.filter(
            on_post=instance.on_post.id, on_comment=instance.on_comment.id
        )
        current_user_commented = total_replies.filter(
            user=request.user
        ).exists()

        data["id"] = instance.id
        data["user_id"] = instance.user.id
        data["username"] = instance.user.profile.username
        data["email"] = instance.user.email
        data["profile_image"] = request.build_absolute_uri(
            instance.user.profile.profile_image.url
        )
        data["on_post"] = instance.on_post.id
        data["on_comment"] = instance.on_comment.id
        data["text"] = instance.text
        data["files"] = request.build_absolute_uri(
            instance.files.url
        ) if instance.files else None
        data["created"] = instance.created()
        data["updated"] = instance.updated()
        data["current_user_action"] = current_user_action
        data["total_popularities"] = comment_remarks.count()
        data["popularity_count"] = {
            "likes": likes.count(),
            "hearts": hearts.count(),
            "funny": funny.count(),
            "insightful": insightful.count(),
            "disappoint": disappoint.count()
        },
        data["popularity_details"] = popularity_details
        data["total_replies"] = total_replies.count()
        data["current_user_commented"] = current_user_commented
        data["child"] = get_replies(instance, request)

        for remark in comment_remarks:
            popularity_details.append({
                "id": remark.id,
                "user_id": remark.user.id,
                "username": remark.user.profile.username,
                "email": remark.user.email,
                "profile_image": request.build_absolute_uri(
                    remark.user.profile.profile_image.url
                ),
                "on_comment": remark.on_comment.id,
                "poularity": remark.popularity,
                "created": remark.created(),
                "updated": remark.updated()
            })

        return data

    def create(self, validated_data):
        user = self.context["request"].user
        return Comments.objects.create(user=user, **validated_data)
