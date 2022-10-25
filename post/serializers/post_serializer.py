from rest_framework import serializers

from post.models.post_model import Post
from post.models.postremark_model import Comments, PostRemark


class PostSerializer(serializers.ModelSerializer):
    like = serializers.SerializerMethodField()
    dislike = serializers.SerializerMethodField()
    current_user_like = serializers.SerializerMethodField()
    current_user_dislike = serializers.SerializerMethodField()
    popularities = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"
        fields = (
            "id", "user", "text", "files", "like", "dislike",
            "current_user_like", "current_user_dislike", "popularities",
            "comments", "created", "updated"
        )
        extra_kwargs = {
            "user": {"read_only": True},
            "title": {"required": False},
            "text": {"required": False},
            "files": {"required": False}
        }

    def get_like(self, obj):
        return PostRemark.objects.filter(
            popularity=PostRemark.Popularity.LIKE, on_post=obj.id
        ).count()

    def get_dislike(self, obj):
        return PostRemark.objects.filter(
            popularity=PostRemark.Popularity.DISLIKE, on_post=obj.id
        ).count()

    def get_current_user_like(self, obj):
        user = self.context["request"].user
        return PostRemark.objects.filter(
            popularity=PostRemark.Popularity.LIKE, on_post=obj.id,
            user=user
        ).exists()

    def get_current_user_dislike(self, obj):
        user = self.context["request"].user
        return PostRemark.objects.filter(
            popularity=PostRemark.Popularity.DISLIKE, on_post=obj.id,
            user=user
        ).exists()

    def get_popularities(self, obj):
        request = self.context["request"]
        for remarks in PostRemark.objects.filter(on_post=obj.id):
            return [{
                "id": remarks.id,
                "username": remarks.user.profile.username,
                "profile_image": request.build_absolute_uri(
                    remarks.user.profile.profile_image.url
                ),
                "on_post": obj.id,
                "popularity": remarks.popularity,
                "created": remarks.created(),
                "updated": remarks.updated()
            }]

    def get_comments(self, obj):
        request = self.context["request"]
        for comment in Comments.objects.filter(on_post=obj):
            return [{
                "id": comment.id,
                "username": comment.user.profile.username,
                "profile_image": request.build_absolute_uri(
                    comment.user.profile.profile_image.url
                ),
                "on_post": obj.id,
                "comment": comment.comment,
                "created": comment.created(),
                "updated": comment.updated(),
                "files": comment.files if comment.files else None,
                "child": comment.parent
            }]

    def create(self, validated_data):
        user = self.context["request"].user
        return Post.objects.create(user=user, **validated_data)
