from django.utils import timezone
from django.utils.timesince import timesince
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, status
from rest_framework.response import Response

from friendship.models import FriendshipRequest

from ..serializers import SendFriendShipRequestSerializer, AcceptFriendRequestSerializer
from ..filters.friend_filter import FriendRequestFilter


class SendFriendRequestAPIView(generics.CreateAPIView):
    serializer_class = SendFriendShipRequestSerializer
    queryset = FriendshipRequest.objects.all()


class ListFriendRequestAPIView(generics.ListAPIView):
    serializer_class = SendFriendShipRequestSerializer
    queryset = FriendshipRequest.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_class = FriendRequestFilter

    def get(self, request):
        all_requests = []
        if FriendshipRequest.objects.filter(to_user=request.user).exists():
            friend_request = FriendshipRequest.objects.filter(to_user=request.user)
            for frnd_request in friend_request:
                if frnd_request.viewed is None:
                    FriendshipRequest.objects.update(viewed=timezone.now())
                all_requests.append({
                    "user_id": frnd_request.from_user.id,
                    "from_user": frnd_request.from_user.email,
                    "recieved": timesince(frnd_request.created),
                    "username": frnd_request.from_user.profile.username,
                    "profile_image": request.build_absolute_uri(frnd_request.from_user.profile.profile_image.url),
                    "viewed": timesince(frnd_request.viewed)
                })
            return Response(all_requests, status=status.HTTP_200_OK)
        return Response({"message": "you have empty friend requests"})


class AcceptFriendRequestAPIView(generics.CreateAPIView):
    serializer_class = AcceptFriendRequestSerializer
    queryset = FriendshipRequest.objects.all()

    def post(self, request):
        if FriendshipRequest.objects.filter(to_user=request.user).exists():
            friend_request = FriendshipRequest.objects.filter(to_user=request.user)
            for frnd_request in friend_request:
                frnd_request.accept()
                return Response({"message": "request accepted"}, status=status.HTTP_201_CREATED)
        return Response({"message": "request does not exists"}, status=status.HTTP_400_BAD_REQUEST)
