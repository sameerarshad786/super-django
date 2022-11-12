from rest_framework import generics, status
from rest_framework.response import Response

from friendship.models import FriendshipRequest, Friend, Follow

from ..serializers import (
    FriendShipRequestSerializer, FriendsSerializer
)


class SendFriendRequestAPIView(generics.CreateAPIView):
    serializer_class = FriendShipRequestSerializer
    queryset = FriendshipRequest.objects.all()


class RecievedRequestAPIView(generics.ListAPIView):
    serializer_class = FriendShipRequestSerializer

    def get_queryset(self):
        return FriendshipRequest.objects.filter(
            to_user=self.request.user
        ).order_by("-created")


class SentRequestsAPIView(generics.ListAPIView):
    serializer_class = FriendShipRequestSerializer

    def get_queryset(self):
        return FriendshipRequest.objects.filter(
            from_user=self.request.user
        ).order_by("-created")


class AcceptFriendRequestAPIView(generics.CreateAPIView):
    serializer_class = FriendShipRequestSerializer
    queryset = FriendshipRequest.objects.all()

    def post(self, request):
        friend_request = FriendshipRequest.objects.filter(
            to_user=request.user
        )
        if friend_request.exists():
            for frnd_request in friend_request:
                if not Follow.objects.followers(frnd_request.from_user):
                    Follow.objects.add_follower(
                        request.user, frnd_request.from_user
                    )

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

    def get_queryset(self):
        return Friend.objects.filter(
            from_user=self.request.user
        ).order_by("-created")


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
