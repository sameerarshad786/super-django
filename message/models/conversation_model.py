from django.db import models

from core.mixins import UUID
from core.models import User


def conversation_photo_path(instance, filename):
    return f"conversation/{instance.id}/{filename}"


class Conversation(UUID):
    participants = models.ManyToManyField(User)


class GroupConversation(UUID):
    participants = models.ManyToManyField(User)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="created_by", null=True
    )
    name = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to=conversation_photo_path,
        default="group_conversation/default-conversation.png"
    )
