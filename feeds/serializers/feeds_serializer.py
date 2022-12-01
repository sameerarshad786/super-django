from rest_framework import serializers

from ..models import Feeds


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feeds
        fields = ("id", "user", "text", "files", "created", "updated")
        extra_kwargs = {
            "user": {"read_only": True},
            "text": {"required": False},
            "files": {"required": False}
        }

    def create(self, validated_data):
        user = self.context["request"].user
        return Feeds.objects.create(user=user, **validated_data)
