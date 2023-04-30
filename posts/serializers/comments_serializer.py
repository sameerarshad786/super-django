from rest_framework import serializers

from ..models import Comments
from ..service import comment_popularities, user_replied, total_replies
from profiles.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    comment_popularities = serializers.JSONField(read_only=True)
    user_replied = serializers.BooleanField(read_only=True)
    total_replies = serializers.IntegerField(read_only=True)
    user_details = UserSerializer(read_only=True, source="user.profile")
    child = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = (
            "id",
            "user",
            "user_details",
            "post",
            "parent",
            "comment",
            "files",
            "comment_popularities",
            "user_replied",
            "total_replies",
            "child",
            "created",
            "updated"
        )
        extra_kwargs = {
            "user": {"read_only": True}
        }

    def get_child(self, obj):
        request = self.context['request']
        query = Comments.objects.filter(parent=obj)
        query = comment_popularities(query, request)
        query = user_replied(query, request)
        query = total_replies(query)
        return CommentSerializer(
            query, context={'request': request}, many=True
        ).data

    def create(self, validated_data):
        user = self.context["request"].user
        return Comments.objects.create(user=user, **validated_data)
