import json

from google.cloud import dialogflow_v2 as dialogflow

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from message.models import BotMessages


@sync_to_async
def delete_old_discussion(user):
    try:
        bot_messages = BotMessages.objects.get(user=user, is_delete=False)
        bot_messages.is_delete = True
        bot_messages.save()
    except BotMessages.DoesNotExist:
        pass


def get_active_bot(user):
    try:
        bot_messages = BotMessages.objects.get(user=user, is_delete=False)

    except BotMessages.DoesNotExist:
        bot_messages = BotMessages(user=user)
        bot_messages.save()

    return bot_messages


@sync_to_async
def first_from_bot(user, session_id):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(
        "newagent-qscn", session_id)
    text_input = dialogflow.types.TextInput(
        text=f"hi {user.profile.full_name}",
        language_code="en-US"
    )
    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session,
        query_input=query_input
    )
    bot_messages = get_active_bot(user)
    bot_messages.discussion.append(
        {"client": "hi", "machine": response.query_result.fulfillment_text}
    )
    bot_messages.save()
    return response.query_result.fulfillment_text


@sync_to_async
def get_bot_response(text, session_id, user):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path("newagent-qscn", session_id)
    text_input = dialogflow.types.TextInput(
        text=text.lower(),
        language_code="en-US"
    )
    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session,
        query_input=query_input
    )
    bot_messages = get_active_bot(user)
    bot_messages.discussion.append(
        {"client": text, "machine": response.query_result.fulfillment_text}
    )
    bot_messages.save()
    return response.query_result.fulfillment_text


class ChatBotConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.user = self.scope["user"]
        self.session_id = self.scope["session_id"]
        self.message = await first_from_bot(self.user, self.session_id)
        await self.send(json.dumps({"machine": self.message}))

    async def disconnect(self, close_code):
        await delete_old_discussion(self.user)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text = text_data_json["client"]
        response = await get_bot_response(
            text, self.session_id, self.user
        )
        await self.send(json.dumps({"machine": response}))
