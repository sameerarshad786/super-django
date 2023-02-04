from django.db.models import Value, F
from django.db.models.functions import Concat, Now
from django.db import models
from django.conf import settings

from rest_framework import generics, status
from rest_framework.response import Response

from ..serializers import FollowSerializer
from ..service.querysets import created_

from friendship.models import Follow


class FollowersAPIView(generics.ListAPIView):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()

    def get(self, request, *args, **kwargs):
        followers = Follow.objects.filter(
            followee=kwargs["user_id"]
        ).annotate(
            profile_picture=Concat(
                Value(settings.MEDIA_BUCKET_URL),
                F("follower__profile__profile_image"),
                output_field=models.URLField()
            ),
            profile_link=Concat(
                Value(settings.PROFILE_URL),
                F("follower__profile__username"),
                output_field=models.URLField()
            )
        ).annotate(
            created_at=Now() - F("created"),
            followed=created_
        ).values(
            "id", "follower_id", "follower__profile__username",
            "profile_picture", "profile_link", "followed"
        )
        return Response(followers, status=status.HTTP_200_OK)


class FollowingsAPIView(generics.ListAPIView):
    serializer_class = FollowSerializer

    def get(self, request, *args, **kwargs):
        followings = Follow.objects.filter(
            follower=kwargs["user_id"]
        ).annotate(
            profile_picture=Concat(
                Value(settings.MEDIA_BUCKET_URL),
                F("followee__profile__profile_image"),
                output_field=models.URLField()
            ),
            profile_link=Concat(
                Value(settings.PROFILE_URL),
                F("followee__profile__username"),
                output_field=models.URLField()
            )
        ).annotate(
            created_at=Now() - F("created"),
            followed=created_
        ).values(
            "id", "followee_id", "followee__profile__username",
            "profile_picture", "profile_link", "followed"
        )
        return Response(followings, status=status.HTTP_200_OK)


class FollowUserAPIView(generics.CreateAPIView):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()


class UnFollowUserAPIView(generics.DestroyAPIView):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()

    def destroy(self, request, *args, **kwargs):
        followee = Follow.objects.filter(
            followee=kwargs["user_id"], follower=request.user
        )
        if followee.exists():
            followee.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {"message": "you cant follow this user"},
            status=status.HTTP_400_BAD_REQUEST
        )
