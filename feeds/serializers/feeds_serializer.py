from rest_framework import serializers

from ..models import Feeds, Remarks, Comments, Popularity
from ..service import get_replies


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feeds
        fields = ("id", "user", "text", "files", "created", "updated")
        extra_kwargs = {
            "user": {"read_only": True},
            "text": {"required": False},
            "files": {"required": False}
        }

    def to_representation(self, instance):
        request = self.context["request"]
        _comments = []
        popularity_details = []
        feed_remarks = []
        data = dict()

        # post remarks
        post_remarks = Remarks.objects.filter(
            on_post=instance, on_comment=None
        )
        current_user_action = post_remarks.filter(
            user=request.user
        ).values("popularity")
        likes = post_remarks.filter(popularity=Popularity.LIKE)
        hearts = post_remarks.filter(popularity=Popularity.HEART)
        funny = post_remarks.filter(popularity=Popularity.FUNNY)
        insightful = post_remarks.filter(popularity=Popularity.INSIGHTFUL)
        disappoint = post_remarks.filter(popularity=Popularity.DISAPPOINT)
        total_comments = Comments.objects.filter(on_post=instance)
        current_user_commented = total_comments.filter(user=request.user)

        for remark in post_remarks:
            feed_remarks.append({
                "id": remark.id,
                "user_id": remark.user.id,
                "username": remark.user.profile.username,
                "email": remark.user.email,
                "profile_image": request.build_absolute_uri(
                    remark.user.profile.profile_image.url
                ),
                "on_post": remark.on_post.id,
                "popularity": remark.popularity,
                "created": remark.created(),
                "updated": remark.updated()
            })

        # post
        data["id"] = instance.id
        data["user_id"] = instance.user.id
        data["username"] = instance.user.profile.username
        data["email"] = instance.user.email
        data["profile_image"] = request.build_absolute_uri(
            instance.user.profile.profile_image.url
        )
        data["text"] = instance.text
        data["files"] = request.build_absolute_uri(
            instance.files.url
        ) if instance.files else None,
        data["created"] = instance.created()
        data["updated"] = instance.updated()
        data["current_user_action"] = current_user_action
        data["total_popularities"] = post_remarks.count()
        data["popularity_count"] = {
            "likes": likes.count(),
            "hearts": hearts.count(),
            "funny": funny.count(),
            "insightful": insightful.count(),
            "disappoint": disappoint.count()
        }
        data["popularity_details"] = feed_remarks
        data["current_user_commented"] = current_user_commented.exists()
        data["total_comments"] = total_comments.count()
        data["comments"] = _comments

        # comments
        comments = Comments.objects.filter(on_post=instance, on_comment=None)
        for comment in comments:
            replies = Comments.objects.filter(
                on_post=instance, on_comment=comment.id
            )
            popularities = Remarks.objects.filter(
                on_post=instance, on_comment=comment.id
            )
            likes = popularities.filter(popularity=Popularity.LIKE)
            hearts = popularities.filter(popularity=Popularity.HEART)
            funny = popularities.filter(popularity=Popularity.FUNNY)
            insightful = popularities.filter(popularity=Popularity.INSIGHTFUL)
            disappoint = popularities.filter(popularity=Popularity.DISAPPOINT)
            current_user_action = popularities.filter(
                user=request.user
            ).values("popularity")
            _comments.append({
                "id": comment.id,
                "user_id": comment.user.id,
                "username": comment.user.profile.username,
                "email": comment.user.email,
                "profile_image": request.build_absolute_uri(
                    comment.user.profile.profile_image.url
                ),
                "on_post": comment.on_post.id,
                "on_comment": None,
                "text": comment.text,
                "files": request.build_absolute_uri(
                    comment.files.url
                ) if comment.files else None,
                "created": comment.created(),
                "updated": comment.updated(),
                "current_user_action": current_user_action,
                "total_popularities": popularities.count(),
                "popularity_count": {
                    "likes": likes.count(),
                    "hearts": hearts.count(),
                    "funny": funny.count(),
                    "insightful": insightful.count(),
                    "disappoint": disappoint.count()
                },
                "popularity_details": popularity_details,
                "total_replies": replies.count(),
                "child": get_replies(comment, request)
            })

            # comment remarks
            comment_remarks = Remarks.objects.filter(on_comment=comment.id)
            for remark in comment_remarks:
                popularity_details.append({
                    "id": remark.id,
                    "user_id": remark.user.id,
                    "user_email": remark.user.email,
                    "username": remark.user.profile.username,
                    "profile_image": request.build_absolute_uri(
                        remark.user.profile.profile_image.url
                    ),
                    "on_comment": comment.id,
                    "on_post": comment.on_post.id,
                    "popularity": remark.popularity,
                    "created_at": remark.created(),
                    "updated_at": remark.updated()
                })

        return data

    def create(self, validated_data):
        user = self.context["request"].user
        return Feeds.objects.create(user=user, **validated_data)
