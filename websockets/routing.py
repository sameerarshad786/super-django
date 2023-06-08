from django.urls import re_path

from channels.routing import URLRouter

from . import consumers


USER_STATUS_PATTERN = [
    re_path(r"user-status/", consumers.UserStatus.as_asgi())
]

websocket_urlpatterns = [
    re_path(r"ws/chat/", consumers.ChatConsumer.as_asgi()),
    re_path(r"ws/", URLRouter(USER_STATUS_PATTERN))
]
