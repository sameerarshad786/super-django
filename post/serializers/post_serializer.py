from rest_framework import serializers

from post.models.post_model import Post
from post.models.remarks_model import Comments, PostRemarks, Popularity, CommentRemarks


class PostSerializer(serializers.ModelSerializer):
    popularities = serializers.SerializerMethodField()
    current_user_action = serializers.SerializerMethodField()
    popularity_details = serializers.SerializerMethodField()
    total_popularities = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id", "user", "text", "files", "popularities",
            "current_user_action", "created", "updated", "total_popularities",
            "popularity_details", "total_comments", "comments"
        )
        extra_kwargs = {
            "user": {"read_only": True},
            "title": {"required": False},
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

        result = {
            "likes": likes,
            "hearts": hearts,
            "funny": funny,
            "insightful": insightful,
            "disappoint": disappoint
        }
        return result

    def get_current_user_action(self, obj):
        user = self.context["request"].user
        like = PostRemarks.objects.filter(
            popularity=Popularity.LIKE, on_post=obj,
            user=user
        ).exists()
        heart = PostRemarks.objects.filter(
            popularity=Popularity.HEART, on_post=obj,
            user=user
        ).exists()
        funny = PostRemarks.objects.filter(
            popularity=Popularity.FUNNY, on_post=obj,
            user=user
        ).exists()
        insightful = PostRemarks.objects.filter(
            popularity=Popularity.INSIGHTFUL, on_post=obj,
            user=user
        ).exists()
        disappoint = PostRemarks.objects.filter(
            popularity=Popularity.DISAPPOINT, on_post=obj,
            user=user
        ).exists()

        result = {
            "like": like,
            "hearts": heart,
            "funny": funny,
            "insightful": insightful,
            "disappoint": disappoint
        }
        return result

    def get_total_popularities(self, obj):
        return PostRemarks.objects.filter(
            on_post=obj
        ).count()

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
                ) if remarks.user.profile.profile_image else None,
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
        result = []
        for comment in comments:
            _remarks = CommentRemarks.objects.filter(on_comment=comment.id)
            result.append({
                "id": comment.id,
                "user_id": comment.user.id,
                "user_email": comment.user.email,
                "username": comment.user.profile.username,
                "profile_image": request.build_absolute_uri(
                    comment.user.profile.profile_image.url
                ) if comment.user.profile.profile_image else None,
                "on_post": obj.id,
                "comment": comment.comment,
                "files": request.build_absolute_uri(
                    comment.files.url) if comment.files else None,
                "created": comment.created(),
                "updated": comment.updated(),
                "total_popularities": _remarks.count(),
                # "popularity_details": result["popularity_details"].append({
                #     "id": remark.id,
                #     "user_id": remark.user.id,
                #     "user_email": remark.user.email,
                #     "username": remark.user.profile.username,
                #     "profile_image": request.build_absolute_uri(
                #         remark.user.profile.profile_image.url
                #     ) if remark.user.profile.profile_image else None,
                #     "on_comment": comment.id,
                #     "action": remark.popularity,
                #     "created_at": remark.created(),
                #     "updated_at": remark.updated()
                # }),
                "parent": Comments.get_replies(comment)
            })
        return result

    def create(self, validated_data):
        user = self.context["request"].user
        return Post.objects.create(user=user, **validated_data)
