from rest_framework import generics, status
from rest_framework.response import Response

from ..serializers import BlockUserSerializer
from ..utils import get_timesince

from friendship.models import Block


class BlockedListAPIView(generics.ListAPIView):
    serializer_class = BlockUserSerializer
    queryset = Block.objects.all()

    def get(self, request, *args, **kwargs):
        blocked_users = Block.objects.filter(blocker=self.request.user)
        result = []
        for blocked_user in blocked_users:
            result.append({
                "id": blocked_user.id,
                "user_id": blocked_user.blocked.id,
                "username": blocked_user.blocked.profile.username,
                "email": blocked_user.blocked.email,
                "profile_image": request.build_absolute_uri(
                    blocked_user.blocked.profile.profile_image.url),
                "followed": get_timesince(blocked_user.created)
            })
        return Response(result)


class BlockUserAPIView(generics.CreateAPIView):
    serializer_class = BlockUserSerializer
    queryset = Block.objects.all()


class UnBlockUserAPIView(generics.DestroyAPIView):
    serializer_class = BlockUserSerializer
    queryset = Block.objects.all()

    def destroy(self, request, *args, **kwargs):
        blocked_user = Block.objects.filter(blocked=kwargs["blocked_id"])
        if blocked_user.exists():
            blocked_user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"message": "block list is empty"}, status=status.HTTP_200_OK
        )
