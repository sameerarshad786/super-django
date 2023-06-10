from rest_framework import serializers

from ..models import Conversation, Messages
from profiles.serializers import UserSerializer


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    latest_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ("id", "participants", "latest_message")

    def get_participants(self, obj):
        user = self.context["user"]
        request = self.context["request"]
        return UserSerializer(
            obj.participants.exclude(id=user.id).distinct(),
            many=True,
            context={"request": request}
        ).data

    def get_latest_message(self, obj):
        user = self.context["user"]
        data = dict()
        data["message"] = {}
        try:
            instance = obj.messages_set.filter(
                to_user=user).latest('created_at')
            data["message"] = instance.get_message()
        except Messages.DoesNotExist:
            pass
        return data
