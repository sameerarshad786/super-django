from django.utils import timezone

from rest_framework import generics, status
from rest_framework.response import Response

from friendship.models import FriendshipRequest, Friend

from ..serializers import FriendSerializer, FriendShipRequestSerializer


class SendFriendRequestAPIView(generics.CreateAPIView):
    serializer_class = FriendSerializer
    queryset = Friend.objects.all()

class ListFriendRequestAPIView(generics.ListAPIView):
    serializer_class = FriendShipRequestSerializer

    def get_queryset(self):
        return FriendshipRequest.objects.filter(to_user=self.request.user)


class FriendRequestAcceptAPIView(generics.CreateAPIView):
    serializer_class = FriendSerializer
    queryset = FriendshipRequest.objects.all()


class RetrieveFriendRequestAPIView(generics.RetrieveAPIView):
    serializer_class = FriendShipRequestSerializer

    def get_queryset(self):
        friend_request = FriendshipRequest.objects.get(to_user=self.request.user)
        if friend_request.viewed == None:
            FriendshipRequest.objects.update(viewed=timezone.now())
        return FriendshipRequest.objects.filter(to_user=self.request.user)
