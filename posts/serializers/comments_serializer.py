from rest_framework import serializers

from ..models import Comments
from ..service import comment_popularities, user_replied, total_replies
from profiles.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    comment_popularities = serializers.JSONField(read_only=True)
    user_replied = serializers.BooleanField(read_only=True)
    total_replies = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    child = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = (
            "id",
            "user",
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
            "post": {"read_only": True}
        }

    def get_child(self, obj):
        request = self.context['request']
        query = Comments.objects.filter(parent=obj)
        query = comment_popularities(query, request.user)
        query = user_replied(query, request.user)
        query = total_replies(query)
        return CommentSerializer(
            query, context={'request': request}, many=True
        ).data

    def create(self, validated_data):
        user = self.context["request"].user
        post_id = self.context["post_id"]
        return Comments.objects.create(
            user=user, post_id=post_id, **validated_data)
