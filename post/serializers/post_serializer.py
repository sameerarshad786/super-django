from django.utils.translation import gettext_lazy as _

from rest_framework import serializers, exceptions

from post.models.post_model import Post
from post.models.postremark_model import Comments, PostRemark


class PostSerializer(serializers.ModelSerializer):
    like = serializers.SerializerMethodField()
    dislike = serializers.SerializerMethodField()
    current_user_like = serializers.SerializerMethodField()
    current_user_dislike = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id", "user", "title", "text", "other_files", "like",
            "dislike", "current_user_like", "current_user_dislike",
            "comments", "created", "updated"
        )
        extra_kwargs = {
            "user": {"read_only": True},
            "title": {"required": False},
            "text": {"required": False},
            "other_files": {"required": False}
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
            popularity=PostRemark.Popularity.LIKE, on_post=obj.id, user=user
        ).exists()

    def get_current_user_dislike(self, obj):
        user = self.context["request"].user
        return PostRemark.objects.filter(
            popularity=PostRemark.Popularity.DISLIKE, on_post=obj.id, user=user
        ).exists()

    def get_comments(self, obj):
        return Comments.objects.all().values()

    def create(self, validated_data):
        user = self.context["request"].user
        return Post.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user = self.context["request"].user
        if user == instance.user:
            return super().update(instance, validated_data)
        raise exceptions.PermissionDenied(_(
            "403 forbidden"
        ))
