from rest_framework import serializers

from ..models import Posts


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True},
            "text": {"required": False},
            "files": {"required": False}
        }

    def create(self, validated_data):
        user = self.context["request"].user
        return Posts.objects.create(user=user, **validated_data)
