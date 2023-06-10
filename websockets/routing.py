from django.urls import path

from channels.routing import URLRouter

from . import consumers


USER_STATUS_URLS_PATTERN = [
    path("online-users/", consumers.TrackOnlineUsers.as_asgi())
]

CHAT_URLS_PATTERNS = [
    path("chat-bot/", consumers.ChatBotConsumer.as_asgi()),
    path("", consumers.ChatConsumer.as_asgi()),
    path("get-latest-conversations/", consumers.ConversationConsumer.as_asgi())
]

MAIN_URLS_PATTERNS = [
    path("user/", URLRouter(USER_STATUS_URLS_PATTERN)),
    path("chat/", URLRouter(CHAT_URLS_PATTERNS))
]

websocket_urlpatterns = [
    path("ws/", URLRouter(MAIN_URLS_PATTERNS))
]
