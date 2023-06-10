import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from message.models import Conversation
from message.serializers import ConversationSerializer
from ..http_request import request


@sync_to_async
def get_all_conversations(user):
    return ConversationSerializer(
        Conversation.objects.filter(
            participants__in=[user]
        ).order_by("-messages__created_at"),
        many=True,
        context={"request": request(), "user": user}
    ).data


class ConversationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.user = self.scope["user"]
        self.all_conversations = await get_all_conversations(self.user)
        await self.send(
            json.dumps({"all_conversations": self.all_conversations}))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        all_conversations = await get_all_conversations(self.user)
        await self.send(
            json.dumps({"all_conversations": all_conversations}))
