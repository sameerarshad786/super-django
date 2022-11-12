from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from post.models.post_model import Post
from post.models.remarks_model import (
    Comments, PostRemarks, Popularity, CommentRemarks
)


class PostSerializer(serializers.ModelSerializer):
    popularities = serializers.SerializerMethodField()
    popularity_details = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id", "user", "text", "files", "popularities", "created",
            "updated", "popularity_details", "total_comments", "comments"
        )
        extra_kwargs = {
            "user": {"read_only": True},
            "text": {"required": False},
            "files": {"required": False}
        }

    def get_popularities(self, obj):
        likes = PostRemarks.objects.filter(
            popularity=Popularity.LIKE, on_post=obj
        ).count()
        hearts = PostRemarks.objects.filter(
            popularity=Popularity.HEART, on_post=obj
        ).count()
        funny = PostRemarks.objects.filter(
            popularity=Popularity.FUNNY, on_post=obj
        ).count()
        insightful = PostRemarks.objects.filter(
            popularity=Popularity.INSIGHTFUL, on_post=obj
        ).count()
        disappoint = PostRemarks.objects.filter(
            popularity=Popularity.DISAPPOINT, on_post=obj
        ).count()
        total_popularities = PostRemarks.objects.filter(
            on_post=obj
        ).count()

        current_user_action = PostRemarks.objects.filter(
            on_post=obj, user=self.context["request"].user
        ).values("popularity")

        return {
            "likes": likes,
            "hearts": hearts,
            "funny": funny,
            "insightful": insightful,
            "disappoint": disappoint,
            "total_popularities": total_popularities,
            "current_user_action": current_user_action
        }

    def get_popularity_details(self, obj):
        request = self.context["request"]
        result = []
        for remarks in PostRemarks.objects.filter(on_post=obj):
            result.append({
                "id": remarks.id,
                "user_id": remarks.user.id,
                "user_email": remarks.user.email,
                "username": remarks.user.profile.username,
                "profile_image": request.build_absolute_uri(
                    remarks.user.profile.profile_image.url
                ),
                "on_post": obj.id,
                "created": remarks.created(),
                "updated": remarks.updated(),
            })
        return result

    def get_total_comments(self, obj):
        return Comments.objects.filter(on_post=obj).count()

    def get_comments(self, obj):
        comments = Comments.objects.filter(on_post=obj, parent=None)
        request = self.context["request"]
        result = {
            "comment": [],
            "popularities": []
        }
        for comment in comments:
            _remarks = CommentRemarks.objects.filter(on_comment=comment.id)
            total_replies = Comments.objects.filter(
                on_post=obj, parent=comment.id
            ).count()
            current_user_action = CommentRemarks.objects.filter(
                on_post=obj, on_comment=comment, user=request.user
            ).values("popularity")
            result["comment"].append({
                "id": comment.id,
                "user_id": comment.user.id,
                "user_email": comment.user.email,
                "username": comment.user.profile.username,
                "profile_image": request.build_absolute_uri(
                    comment.user.profile.profile_image.url
                ),
                "on_post": obj.id,
                "comment": comment.comment,
                "files": request.build_absolute_uri(
                    comment.files.url) if comment.files else None,
                "created": comment.created(),
                "updated": comment.updated(),
                "total_popularities": _remarks.count(),
                "current_user_action": current_user_action,
                "total_replies": total_replies,
                "parent": Comments.get_replies(comment)
            })
            for remark in _remarks:
                result["popularities"].append({
                    "id": remark.id,
                    "user_id": remark.user.id,
                    "user_email": remark.user.email,
                    "username": remark.user.profile.username,
                    "profile_image": request.build_absolute_uri(
                        remark.user.profile.profile_image.url
                    ),
                    "on_comment": comment.id,
                    "popularity": remark.popularity,
                    "created_at": remark.created(),
                    "updated_at": remark.updated()
                }),
        return result

    def create(self, validated_data):
        user = self.context["request"].user
        if not user.profile.username:
            raise serializers.ValidationError(_("Update your profile first"))
        return Post.objects.create(user=user, **validated_data)
