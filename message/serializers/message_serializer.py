from rest_framework import serializers

from ..models.message_models import Messages
from profiles.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(required=True)
    child = serializers.SerializerMethodField()

    class Meta:
        model = Messages
        fields = (
            "id",
            "from_user",
            "to_user",
            "message",
            "file",
            "parent",
            "is_seen",
            "child",
            "conversation_on"
        )

    def get_child(self, obj):
        request = self.context['request']
        query = Messages.objects.filter(parent=obj)
        return MessageSerializer(
            query, context={'request': request}, many=True
        ).data
