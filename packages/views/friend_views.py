from rest_framework import generics, status
from rest_framework.response import Response

from friendship.models import FriendshipRequest, Friend

from ..serializers import (
    FriendShipRequestSerializer, FriendsSerializer
)
from ..utils import get_timesince


class SendFriendRequestAPIView(generics.CreateAPIView):
    serializer_class = FriendShipRequestSerializer
    queryset = FriendshipRequest.objects.all()


class ListFriendRequestAPIView(generics.ListAPIView):
    serializer_class = FriendShipRequestSerializer
    queryset = FriendshipRequest.objects.all()

    def get(self, request):
        all_requests = []
        if FriendshipRequest.objects.filter(to_user=request.user).exists():
            friend_request = FriendshipRequest.objects.filter(
                to_user=request.user)
            for frnd_request in friend_request:
                if frnd_request.viewed is None:
                    frnd_request.mark_viewed()
                all_requests.append({
                    "user_id": frnd_request.from_user.id,
                    "from_user": frnd_request.from_user.email,
                    "recieved": get_timesince(frnd_request.created),
                    "username": frnd_request.from_user.profile.username,
                    "profile_image": request.build_absolute_uri(
                        frnd_request.from_user.profile.profile_image.url),
                    "viewed": get_timesince(frnd_request.viewed)
                })
            return Response(all_requests, status=status.HTTP_200_OK)
        return Response({"message": "you have empty friend requests"})


class AcceptFriendRequestAPIView(generics.CreateAPIView):
    serializer_class = FriendShipRequestSerializer
    queryset = FriendshipRequest.objects.all()

    def post(self, request):
        if FriendshipRequest.objects.filter(to_user=request.user).exists():
            friend_request = FriendshipRequest.objects.filter(
                to_user=request.user)
            for frnd_request in friend_request:
                frnd_request.accept()
                return Response({"message": "Request Accepted"})
        return Response(
            {"message": "request does not exists"},
            status=status.HTTP_400_BAD_REQUEST
        )


class AllFriendListAPIView(generics.ListAPIView):
    serializer_class = FriendsSerializer
    queryset = Friend.objects.all()

    def get(self, request, *args, **kwargs):
        friend = Friend.objects.filter(to_user=self.request.user)
        if friend.exists():
            data = []
            for friends in friend:
                data.append({
                    "id": friends.id,
                    "user_id": friends.from_user.id,
                    "username": friends.from_user.profile.username,
                    "from_user": friends.from_user.email,
                    "profile_image": request.build_absolute_uri(
                        friends.from_user.profile.profile_image.url
                    ),
                    "friends": get_timesince(friends.created)
                })
            return Response(data, status=status.HTTP_200_OK)
        return Response(
            {"message": "You have empty friend list"},
            status=status.HTTP_200_OK
        )
