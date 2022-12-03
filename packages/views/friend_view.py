from django.db.models import Value, F
from django.db.models.functions import Concat, Now
from django.db import models
from django.conf import settings

from rest_framework import generics, status
from rest_framework.response import Response

from friendship.models import FriendshipRequest, Friend, Follow

from ..serializers import (
    FriendShipRequestSerializer, FriendsSerializer
)
from ..service.querysets import created_


class SendFriendRequestAPIView(generics.CreateAPIView):
    serializer_class = FriendShipRequestSerializer
    queryset = FriendshipRequest.objects.all()


class RecievedRequestAPIView(generics.ListAPIView):
    serializer_class = FriendShipRequestSerializer
    queryset = FriendshipRequest.objects.all()

    def get(self, request, *args, **kwargs):
        friendrequests = self.queryset.filter(to_user=request.user).annotate(
            profile_picture=Concat(
                Value(settings.MEDIA_BUCKET_URL),
                F("from_user__profile__profile_image"),
                output_field=models.URLField()
            ),
            profile_link=Concat(
                Value(settings.PROFILE_URL),
                F("from_user__profile__id"),
                output_field=models.URLField()
            )
        ).annotate(
            created_at=Now() - F("created"), recieved=created_
        ).values(
            "id", "from_user", "from_user__profile__username",
            "profile_picture", "profile_link", "recieved"
        )
        return Response(friendrequests, status=status.HTTP_200_OK)


class SentRequestsAPIView(generics.ListAPIView):
    serializer_class = FriendShipRequestSerializer
    queryset = FriendshipRequest.objects.all()

    def get(self, request, *args, **kwargs):
        qs = self.queryset.filter(from_user=request.user).annotate(
            profile_picture=Concat(
                Value(settings.MEDIA_BUCKET_URL),
                F("to_user__profile__profile_image"),
                output_field=models.URLField()
            ),
            profile_link=Concat(
                Value(settings.PROFILE_URL),
                F("to_user__profile__id"),
                output_field=models.URLField()
            )
        ).annotate(
            created_at=Now() - F("created"),
            recieved=created_
        ).values(
            "id", "to_user", "to_user__profile__username",
            "profile_picture", "profile_link", "recieved"
        )
        return Response(qs)


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
    queryset = Friend.objects.all()

    def get(self, request, *args, **kwargs):
        friends = self.queryset.filter(to_user=request.user).annotate(
            profile_picture=Concat(
                Value(settings.MEDIA_BUCKET_URL),
                F("to_user__profile__profile_image"),
                output_field=models.URLField()
            ),
            profile_link=Concat(
                Value(settings.PROFILE_URL),
                F("to_user__profile__id"),
                output_field=models.URLField()
            )
        ).annotate(
            created_at=Now() - F("created"),
            friends=created_
        ).values(
            "id", "from_user", "from_user__profile__username",
            "profile_picture", "profile_link", "friends"
        )
        return Response(friends)


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
