from django.db.models import Value, F
from django.db.models.functions import Concat, Now
from django.db import models
from django.conf import settings

from rest_framework import generics, status
from rest_framework.response import Response

from ..serializers import BlockUserSerializer
from ..service.querysets import created_

from friendship.models import Block


class BlockedListAPIView(generics.ListAPIView):
    serializer_class = BlockUserSerializer
    queryset = Block.objects.all()

    def get(self, request, *args, **kwargs):
        blocked = self.queryset.filter(blocker=self.request.user).annotate(
            profile_picture=Concat(
                Value(settings.MEDIA_BUCKET_URL),
                F("blocked__profile__profile_image"),
                output_field=models.URLField()
            ),
            profile_link=Concat(
                Value(settings.PROFILE_URL),
                F("blocked__profile__id"),
                output_field=models.URLField()
            )
        ).annotate(
            created_at=Now() - F("created"),
            blocke=created_
        ).values(
            "id", "blocked_id", "blocked__profile__username",
            "profile_picture", "profile_link", "blocke"
        )
        return Response(blocked, status=status.HTTP_200_OK)


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
