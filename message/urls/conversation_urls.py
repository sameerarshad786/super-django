from django.urls import path
from .. import views


CONVERSATION_PATTERNS = [
    path(
        "get-conversation/<int:participant_id>/",
        views.GetOrCreateConversation.as_view(),
        name="get-or-create-conversation"
    )
]
