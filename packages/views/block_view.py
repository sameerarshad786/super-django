from rest_framework import generics, status
from rest_framework.response import Response

from ..serializers import BlockUserSerializer

from friendship.models import Block


class BlockedListAPIView(generics.ListAPIView):
    serializer_class = BlockUserSerializer

    def get_queryset(self):
        return Block.objects.filter(
            blocker=self.request.user
        ).order_by("-created")


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
            {"message": "you have not block this user"},
            status=status.HTTP_200_OK
        )
