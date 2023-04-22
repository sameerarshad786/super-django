from rest_framework import serializers

from ..models import Posts
from profiles.serializers import UserSerializer


class Postserializer(serializers.ModelSerializer):
    popularities = serializers.JSONField(read_only=True)
    total_comment = serializers.IntegerField(read_only=True)
    current_user_commented = serializers.BooleanField(read_only=True)
    user_details = UserSerializer(read_only=True, source="user.profile")

    class Meta:
        model = Posts
        fields = (
            "id",
            "user",
            "user_details",
            "text",
            "files",
            "popularities",
            "total_comment",
            "current_user_commented",
            "created",
            "updated"
        )
        extra_kwargs = {
            "user": {"read_only": True}
        }

    def create(self, validated_data):
        user = self.context["request"].user
        return Posts.objects.create(user=user, **validated_data)
