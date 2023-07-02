import json

from django.core.serializers.json import DjangoJSONEncoder

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from message.models import Messages, Conversation
from message.serializers import MessageSerializer
from ..http_request import request
from ..pagination import paginate_response


@sync_to_async
def all_messages(conversation_id):
    messages = MessageSerializer(
        Messages.objects.filter(
            conversation_on_id=conversation_id
        ).order_by("-created_at"),
        many=True,
        context={'request': request()}
    ).data
    return messages


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.user = self.scope["user"]
        self.conversation_id = self.scope["conversation_id"]
        self.parent_id = self.scope["parent_id"]
        conversation = await Conversation.objects.aget(
            id=self.conversation_id)
        self.to_user = await conversation.participants.exclude(
            id=self.user.id).afirst()
        serialized_function = await all_messages(self.conversation_id)
        count = await Messages.objects.filter(
            conversation_on_id=self.conversation_id).acount()
        paginated_response = await paginate_response(
            count, 1, serialized_function)
        await self.send(
            json.dumps({"messages": paginated_response}, cls=DjangoJSONEncoder)
        )

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        page_number = text_data_json.get("page_number", 1)
        if message:
            await Messages.objects.acreate(
                from_user=self.user,
                to_user=self.to_user,
                conversation_on_id=self.conversation_id,
                parent_id=self.parent_id,
                message=message
            )
        count = await Messages.objects.filter(
            conversation_on_id=self.conversation_id).acount()
        serialized_function = await all_messages(self.conversation_id)
        paginated_response = await paginate_response(
            count, page_number, serialized_function)
        await self.send(
            json.dumps({"messages": paginated_response}, cls=DjangoJSONEncoder)
        )
