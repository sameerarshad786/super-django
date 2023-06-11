from django.db.models import Q, Count
from django.db.models.functions import JSONObject
from django.contrib.postgres.aggregates import ArrayAgg

from rest_framework import generics, status
from rest_framework.response import Response

from ..models import Remarks
from ..serializers import RemarkSerializer
from core.permissions import IsOwner
from ..service.custom_db_func import CustomBoolOr
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
            total=Count("pk"),
            like=Count("pk", filter=Q(popularity=Remarks.Popularity.LIKE)),
            heart=Count("pk", filter=Q(popularity=Remarks.Popularity.HEART)),
            funny=Count("pk", filter=Q(popularity=Remarks.Popularity.FUNNY)),
            insightful=Count(
                "pk", filter=Q(popularity=Remarks.Popularity.INSIGHTFUL)),
            disappoint=Count(
                "pk", filter=Q(popularity=Remarks.Popularity.DISAPPOINT)),
            current_user_like=CustomBoolOr(
                Q(user=request.user, popularity=Remarks.Popularity.LIKE)
            ),
            current_user_heart=CustomBoolOr(
                Q(user=request.user, popularity=Remarks.Popularity.HEART)
            ),
            current_user_funny=CustomBoolOr(
                Q(user=request.user, popularity=Remarks.Popularity.FUNNY)
            ),
            current_user_insightful=CustomBoolOr(
                Q(
                    user=request.user,
                    popularity=Remarks.Popularity.INSIGHTFUL
                )
            ),
            current_user_disappoint=CustomBoolOr(
                Q(
                    user=request.user,
                    popularity=Remarks.Popularity.DISAPPOINT
                )
            ),
            user_popularity_details=ArrayAgg(
                JSONObject(
                    id="id",
                    user_id="user_id",
                    username="user__profile__username",
                    popularity="popularity",
                    profile_image=profile_picture,
                    profile_link=profile_link
                )
            )
        )
        return Response(query, status=status.HTTP_200_OK)


class CommentRemarksRetrieveAPIView(generics.ListAPIView):
    serializer_class = RemarkSerializer

    def get(self, request, *args, **kwargs):
        query = Remarks.objects.filter(
            comment=kwargs["comment_id"]
        ).aggregate(
            # https://docs.djangoproject.com/en/4.2/ref/models/conditional-expressions/#conditional-aggregation
            total=Count("pk"),
            like=Count("pk", filter=Q(popularity=Remarks.Popularity.LIKE)),
            heart=Count("pk", filter=Q(popularity=Remarks.Popularity.HEART)),
            funny=Count("pk", filter=Q(popularity=Remarks.Popularity.FUNNY)),
            insightful=Count(
                "pk", filter=Q(popularity=Remarks.Popularity.INSIGHTFUL)),
            disappoint=Count(
                "pk", filter=Q(popularity=Remarks.Popularity.DISAPPOINT)),
            current_user_like=CustomBoolOr(
                Q(user=request.user, popularity=Remarks.Popularity.LIKE)
            ),
            current_user_heart=CustomBoolOr(
                Q(user=request.user, popularity=Remarks.Popularity.HEART)
            ),
            current_user_funny=CustomBoolOr(
                Q(user=request.user, popularity=Remarks.Popularity.FUNNY)
            ),
            current_user_insightful=CustomBoolOr(
                Q(user=request.user, popularity=Remarks.Popularity.INSIGHTFUL)
            ),
            current_user_disappoint=CustomBoolOr(
                Q(user=request.user, popularity=Remarks.Popularity.DISAPPOINT)
            ),
            user_popularity_details=ArrayAgg(
                JSONObject(
                    id="id",
                    user_id="user_id",
                    username="user__profile__username",
                    popularity="popularity",
                    profile_image=profile_picture,
                    profile_link=profile_link
                )
            )
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
