from rest_framework import serializers

from ..models import Comments
from ..service import comment_popularities, user_replied, total_replies


class CommentSerializer(serializers.ModelSerializer):
    comment_popularities = serializers.JSONField(read_only=True)
    user_replied = serializers.BooleanField(read_only=True)
    total_replies = serializers.IntegerField(read_only=True)
    child = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = (
            "id",
            "user",
            "post",
            "comment",
            "text",
            "files",
            "comment_popularities",
            "user_replied",
            "total_replies",
            "child"
        )
        extra_kwargs = {
            "user": {"read_only": True}
        }

    def get_child(self, obj):
        request = self.context['request']
        query = Comments.objects.filter(comment=obj)
        query = comment_popularities(query, request)
        query = user_replied(query, request)
        query = total_replies(query)
        return CommentSerializer(
            query, context={'request': request}, many=True
        ).data

    def to_representation(self, instance):
        request = self.context["request"]
        representation = super().to_representation(instance)
        representation["created"] = instance.created()
        representation["updated"] = instance.updated()
        if request.method == "GET":
            representation["comment_popularities"] = {
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
            representation["total_replies"] = 0 \
                if instance.total_replies is None else instance.total_replies
        return representation

    def create(self, validated_data):
        user = self.context["request"].user
        return Comments.objects.create(user=user, **validated_data)
