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


class RecievedRequestAPIView(generics.ListAPIView):
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
                    "id": frnd_request.id,
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


class SentRequestsAPIView(generics.ListAPIView):
    serializer_class = FriendShipRequestSerializer
    queryset = FriendshipRequest.objects.all()

    def get(self, request, *args, **kwargs):
        sent_requests = FriendshipRequest.objects.filter(
            from_user=self.request.user)
        result = []
        for requests in sent_requests:
            result.append({
                "id": requests.from_user.id,
                "user_id": requests.to_user.id,
                "username": requests.to_user.profile.username,
                "email": requests.to_user.email,
                "sent": get_timesince(requests.created),
                "user_viewed": get_timesince(requests.viewed)
                if requests.viewed else None
            })
        return Response(result, status=status.HTTP_200_OK)


class AcceptFriendRequestAPIView(generics.CreateAPIView):
    serializer_class = FriendShipRequestSerializer
    queryset = FriendshipRequest.objects.all()

    def post(self, request):
        friend_request = FriendshipRequest.objects.filter(
            to_user=request.user
        )
        if friend_request.exists():
            for frnd_request in friend_request:
                frnd_request.accept()
                return Response({"message": "Request Accepted"})
        return Response(
            {"message": "request does not exists"},
            status=status.HTTP_400_BAD_REQUEST
        )


class CancelFriendRequestAPIView(generics.DestroyAPIView):
    serializer_class = FriendShipRequestSerializer
    queryset = FriendshipRequest.objects.all()

    def destroy(self, request, *args, **kwargs):
        friend_request = FriendshipRequest.objects.filter(
            to_user=kwargs["to_user"]
        )
        if friend_request.exists():
            friend_request.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"message": "empty request"},
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


class UnFriendAPIView(generics.DestroyAPIView):
    serializer_class = FriendsSerializer
    queryset = Friend.objects.all()

    def destroy(self, request, *args, **kwargs):
        friend = Friend.objects.filter(
            from_user=request.user, to_user=kwargs["to_user"]
        )
        if friend.exists():
            Friend.objects.filter(
                from_user=kwargs["to_user"], to_user=request.user
            ).delete()
            friend.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"message": "you both are not friends"},
            status=status.HTTP_400_BAD_REQUEST
        )
