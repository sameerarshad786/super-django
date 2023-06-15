from rest_framework import generics, status
from rest_framework.response import Response

from ..serializers import ConversationSerializer
from ..models import Conversation
from core.models import User


class GetOrCreateConversation(generics.GenericAPIView):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.all()

    def get(self, request, *args, **kwargs):
        participant_id = kwargs["participant_id"]
        try:
            user_to_add = User.objects.get(id=participant_id)
            if user_to_add == self.request.user:
                return Response(
                    {"error": "participant can't contain requested user"}
                )
        except User.DoesNotExist:
            return Response(
                {"error": "user with this participant_id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            conversation = Conversation.objects.filter(
                participants__in=[request.user]
            ).filter(participants__in=[user_to_add]).get()
        except Conversation.DoesNotExist:
            conversation = Conversation()
            conversation.save()
            conversation.participants.add(*[request.user.id, user_to_add.id])
        data = {
            "id": conversation.id
        }
        return Response(data, status=status.HTTP_200_OK)
