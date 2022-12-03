from django.db.models import Count, Subquery, OuterRef, F
from django.db.models.functions import JSONObject, Now
from django.contrib.postgres.aggregates import ArrayAgg

from rest_framework import generics, status
from rest_framework.response import Response

from ..models import Remarks, Posts, Comments
from ..serializers import RemarkSerializer
from core.permissions import IsOwner
from ..service.querysets import (
    popularities, profile_picture, profile_link, created_
)


class PostRemarksRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = RemarkSerializer

    def get(self, request, *args, **kwargs):
        current_user_action = Subquery(Remarks.objects.filter(
            post=OuterRef("pk"), comment=None, user=request.user
            ).values("post", "popularity").annotate(
                popularity_=F("popularity")
            ).values("popularity_")
        )

        # https://stackoverflow.com/questions/63020407/return-multiple-values-in-subquery-in-django-orm
        popularity_details = Subquery(Remarks.objects.filter(
            post=OuterRef("pk"), comment=None
            ).values("post").annotate(
                created=Now() - F("created_at"), created_=created_
            ).values("created_").annotate(
                details=ArrayAgg(
                    JSONObject(
                        id="id",
                        user_id="user_id",
                        username="user__profile__username",
                        popularity="popularity",
                        created=F("created_"),
                        profile_image=profile_picture,
                        profile_link=profile_link
                    ),
                )
            ).values("details")
        )

        remark = Subquery(Remarks.objects.filter(
            post=OuterRef("pk"), comment=None
            ).values("post").annotate(count=Count("pk")).annotate(
                popularities=popularities,
            ).values("popularities")
        )

        post = Posts.objects.filter(id=kwargs["post_id"]).annotate(
            current_user_action=current_user_action,
            remark=remark,
            popularity_details=popularity_details
        ).values("remark", "current_user_action", "popularity_details")
        return Response(post, status=status.HTTP_200_OK)


class CommentRemarksRetrieveAPIView(generics.ListAPIView):
    serializer_class = RemarkSerializer

    def get(self, request, *args, **kwargs):
        current_user_action = Subquery(Remarks.objects.filter(
            comment=OuterRef("pk"), user=request.user
            ).values("comment", "popularity").annotate(
                popularity_=F("popularity")
            ).values("popularity_")
        )

        # https://stackoverflow.com/questions/63020407/return-multiple-values-in-subquery-in-django-orm
        popularity_details = Subquery(
            Remarks.objects.filter(
                comment=OuterRef("pk")
            ).values("comment").annotate(
                created=Now() - F("created_at"), created_=created_
            ).values("created_").annotate(
                details=ArrayAgg(
                    JSONObject(
                        id="id",
                        user_id="user_id",
                        username="user__profile__username",
                        popularity="popularity",
                        created=F("created_"),
                        profile_image=profile_picture,
                        profile_link=profile_link
                    ),
                )
            ).values("details")
        )

        remark = Subquery(Remarks.objects.filter(
            comment=OuterRef("pk")
            ).values("comment").annotate(count=Count("pk")).annotate(
                popularities=popularities,
            ).values("popularities")
        )

        comment = Comments.objects.filter(id=kwargs["comment_id"]).annotate(
            current_user_action=current_user_action,
            remark=remark,
            popularity_details=popularity_details
        ).values("remark", "current_user_action", "popularity_details")
        return Response(comment, status=status.HTTP_200_OK)


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
