from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from message.models.conversation_model import Conversation


class ParticipantsCapacityError(Exception):
    pass


@receiver(m2m_changed, sender=Conversation.participants.through)
def handle_participant_change(sender, instance, action, pk_set, **kwargs):
    if action == "pre_add":
        if instance.participants.count() + len(pk_set) > 2:
            raise ParticipantsCapacityError("Max participants capactiy is 2")

    elif action == 'pre_remove':
        pass
