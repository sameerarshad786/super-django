import json

from django.db.models import Q, Count, Value
from django.db.models.functions import JSONObject
from django.contrib.postgres.aggregates import ArrayAgg, BoolOr
from django.db.models import Prefetch

from rest_framework import generics, status
from rest_framework.response import Response

from ..models import Remarks, Posts, Comments
from ..serializers import RemarkSerializer
from core.permissions import IsOwner
from ..service.querysets import (
    profile_picture, profile_link
)


class PostRemarksRetrieveAPIView(generics.ListAPIView):
    serializer_class = RemarkSerializer
    queryset = Remarks.objects.all()

    def get(self, request, *args, **kwargs):
        query = Remarks.objects.filter(
            post=kwargs["post_id"], comment=None
        ).aggregate(
            # https://docs.djangoproject.com/en/4.2/ref/models/conditional-expressions/#conditional-aggregation
            popularities=JSONObject(
                total_actions=Count("pk"),
                like=Count("pk", filter=Q(like=True)),
                heart=Count("pk", filter=Q(heart=True)),
                funny=Count("pk", filter=Q(funny=True)),
                insightful=Count("pk", filter=Q(insightful=True)),
                disappoint=Count("pk", filter=Q(disappoint=True)),
                current_user_like=BoolOr(Q(user=request.user, like=True)),
                current_user_heart=BoolOr(Q(user=request.user, heart=True)),
                current_user_funny=BoolOr(Q(user=request.user, funny=True)),
                current_user_insightful=BoolOr(Q(user=request.user, insightful=True)),
                current_user_disappoint=BoolOr(Q(user=request.user, disappoint=True)),
            ),
            # user_popularity_details=ArrayAgg(
            #     JSONObject(
            #         id="id",
            #         user_id="user_id",
            #         username="user__profile__username",
            #         # popularity="popularity",
            #         profile_image=profile_picture,
            #         profile_link=profile_link
            #     )
            # )
        )
        return Response(query, status=status.HTTP_200_OK)


class CommentRemarksRetrieveAPIView(generics.ListAPIView):
    serializer_class = RemarkSerializer

    def get(self, request, *args, **kwargs):
        query = Remarks.objects.filter(
            comment=kwargs["comment_id"]
        ).select_related("user").prefetch_related(
            Prefetch("comment", queryset=Comments.objects.get(id=kwargs["comment_id"]))
        ).aggregate(
            # https://docs.djangoproject.com/en/4.2/ref/models/conditional-expressions/#conditional-aggregation
            total_actions=Count("pk"),
            like=Count("pk", filter=Q(like=True)),
            heart=Count("pk", filter=Q(heart=True)),
            funny=Count("pk", filter=Q(funny=True)),
            insightful=Count("pk", filter=Q(insightful=True)),
            disappoint=Count("pk", filter=Q(disappoint=True)),
            current_user_like=BoolOr(Q(user=request.user, like=True)),
            current_user_heart=BoolOr(Q(user=request.user, heart=True)),
            current_user_funny=BoolOr(Q(user=request.user, funny=True)),
            current_user_insightful=BoolOr(Q(user=request.user, insightful=True)),
            current_user_disappoint=BoolOr(Q(user=request.user, disappoint=True)),
            # user_popularity_details=ArrayAgg(
            #     JSONObject(
            #         id="id",
            #         user_id="user_id",
            #         username="user__profile__username",
            #         popularity="popularity",
            #         profile_image=profile_picture,
            #         profile_link=profile_link
            #     )
            # )
        )
        return Response(query, status=status.HTTP_200_OK)


class RemarksCreateAPIView(generics.CreateAPIView):
    serializer_class = RemarkSerializer
    queryset = Remarks.objects.all()


class RemarksUpdateAPIView(generics.UpdateAPIView):
    serializer_class = RemarkSerializer
    queryset = Remarks.objects.all()
    permission_classes = (IsOwner, )


class RemarksDeleteAPIView(generics.DestroyAPIView):
    serializer_class = RemarkSerializer
    queryset = Remarks.objects.all()
    permission_classes = (IsOwner, )
