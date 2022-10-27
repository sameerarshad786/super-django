from rest_framework import serializers

from post.models.post_model import Post
from post.models.postremark_model import Comments, PostRemark


class PostSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField()
    total_dislikes = serializers.SerializerMethodField()
    current_user_like = serializers.SerializerMethodField()
    current_user_dislike = serializers.SerializerMethodField()
    popularities = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"
        fields = (
            "id", "user", "text", "files", "total_likes", "total_dislikes",
            "total_comments", "current_user_like", "current_user_dislike",
            "popularities", "comments", "created", "updated"
        )
        extra_kwargs = {
            "user": {"read_only": True},
            "title": {"required": False},
            "text": {"required": False},
            "files": {"required": False}
        }

    def get_total_likes(self, obj):
        return PostRemark.objects.filter(
            popularity=PostRemark.Popularity.LIKE, on_post=obj
        ).count()

    def get_total_dislikes(self, obj):
        return PostRemark.objects.filter(
            popularity=PostRemark.Popularity.DISLIKE, on_post=obj
        ).count()

    def get_current_user_like(self, obj):
        user = self.context["request"].user
        return PostRemark.objects.filter(
            popularity=PostRemark.Popularity.LIKE, on_post=obj,
            user=user
        ).exists()

    def get_current_user_dislike(self, obj):
        user = self.context["request"].user
        return PostRemark.objects.filter(
            popularity=PostRemark.Popularity.DISLIKE, on_post=obj,
            user=user
        ).exists()

    def get_popularities(self, obj):
        request = self.context["request"]
        for remarks in PostRemark.objects.filter(on_post=obj):
            return [{
                "id": remarks.id,
                "user_id": remarks.user.id,
                "username": remarks.user.profile.username,
                "profile_image": request.build_absolute_uri(
                    remarks.user.profile.profile_image.url
                ) if remarks.user.profile.profile_image else None,
                "on_post": obj.id,
                "popularity": remarks.popularity,
                "created": remarks.created(),
                "updated": remarks.updated()
            }]

    def get_total_comments(self, obj):
        return Comments.objects.filter(on_post=obj, parent=None).count()

    def get_comments(self, obj):
        comments = Comments.objects.filter(on_post=obj, parent=None)
        request = self.context["request"]
        result = []
        for comment in comments:
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
                "parent": Comments.get_replies(comment)
            })
        return result

    def create(self, validated_data):
        user = self.context["request"].user
        return Post.objects.create(user=user, **validated_data)
