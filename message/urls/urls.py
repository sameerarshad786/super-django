from django.urls import path, include
from .conversation_urls import CONVERSATION_PATTERNS


urlpatterns = [
    path("conversation/", include(CONVERSATION_PATTERNS))
]
