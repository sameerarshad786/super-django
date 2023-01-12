from rest_framework import serializers

from ..models import Posts


class FeedSerializer(serializers.ModelSerializer):
    popularities = serializers.JSONField(read_only=True)
    current_user_commented = serializers.BooleanField(read_only=True)
    total_comment = serializers.IntegerField(read_only=True)

    class Meta:
        model = Posts
        fields = (
            "id",
            "user",
            "text",
            "files",
            "popularities",
            "total_comment",
            "current_user_commented"
        )
        extra_kwargs = {
            "user": {"read_only": True}
        }

    def to_representation(self, instance):
        request = self.context["request"]
        representation = super().to_representation(instance)
        representation["created"] = instance.created()
        representation["updated"] = instance.updated()
        if request.method == "GET":
            representation["popularities"] = {
                    "like": 0,
                    "funny": 0,
                    "heart": 0,
                    "disappoint": 0,
                    "insightful": 0,
                    "total_actions": 0,
                    "current_user_like": False,
                    "current_user_funny": False,
                    "current_user_heart": False,
                    "current_user_disappoint": False,
                    "current_user_insightful": False
                } if instance.popularities is None else instance.popularities
            representation["total_comments"] = 0 \
                if instance.total_comment is None else instance.total_comment
        return representation

    def create(self, validated_data):
        user = self.context["request"].user
        return Posts.objects.create(user=user, **validated_data)
