from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from post.models.post_model import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("user", "title", "text", 
        "other_files", "created", "updated")
        extra_kwargs = {
            "user": {"read_only": True},
            "title": {"required": False},
            "text": {"required": False},
            "other_files": {"required": False}
        }

    def create(self, validated_data):
        user = self.context["request"].user
        return Post.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user = self.context["request"].user
        if user == instance.user:
            return super().update(instance, validated_data)
        raise serializers.ValidationError(_(
            "403 forbidden"
        ))
