import json

from django.db.models import Max

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from message.models import Conversation
from message.serializers import ConversationSerializer
from ..http_request import Request
from ..pagination import paginate_response


@sync_to_async
def get_all_conversations(user):
    return ConversationSerializer(
        Conversation.objects.filter(participants__in=[user]).annotate(
            latest_from=Max("messages__created_at")
        ).order_by("-latest_from"),
        many=True,
        context={"request": Request(), "user": user}
    ).data


class ConversationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.user = self.scope["user"]
        self.all_conversations = await get_all_conversations(self.user)
        count = await Conversation.objects.filter(
            participants__in=[self.user]).acount()
        paginted_response = await paginate_response(
            count, 1, self.all_conversations)
        await self.send(
            json.dumps({"all_conversations": paginted_response}))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        page_number = text_data_json.get("page_number", 1)
        count = await Conversation.objects.filter(
            participants__in=[self.user]).acount()
        serialized_function = await get_all_conversations(self.user)
        paginted_response = await paginate_response(
            count, page_number, serialized_function)
        await self.send(
            json.dumps({"all_conversations": paginted_response}))
