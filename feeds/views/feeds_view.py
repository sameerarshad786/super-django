from django.db.models import (
    Q, Count, F, Value, Case, When, OuterRef, Subquery
)
from django.db.models.functions import Now, Concat, JSONObject
from django.conf import settings
from django.db import models

from rest_framework import parsers, generics, status
from rest_framework.response import Response

from ..models import Feeds, Remarks, Comments
from ..serializers import FeedSerializer
from core.permissions import IsOwner
from ..tasks.querysets import (
    created_, updated_, profile_link, popularities
)


class FeedsAPIView(generics.ListAPIView):
    serializer_class = FeedSerializer
    queryset = Feeds.objects.all()

    def get(self, request, *args, **kwargs):
        # https://stackoverflow.com/questions/43770118/simple-subquery-with-outerref
        current_user_action = Subquery(Remarks.objects.filter(
            on_post=OuterRef("pk"), on_comment=None, user=request.user
            ).values("on_post", "popularity").annotate(
                popularity_=F("popularity")
            ).values("popularity")
        )

        current_user_commented = Subquery(Comments.objects.filter(
            on_post=OuterRef("pk"), user=request.user
            ).values("on_post").annotate(count=Count("pk")).annotate(
                comment=Case(When(Q(count=F("count")), then=True))
            ).values("comment")
        )

        total_comment = Subquery(Comments.objects.filter(
            on_post=OuterRef("pk")
            ).values("on_post").annotate(count=Count("pk")).annotate(
                total=F("count")
            ).values("total")
        )

        post_remarks = Subquery(Remarks.objects.filter(
                on_post=OuterRef("pk"), on_comment=None
                ).values("on_post").annotate(
                    count=Count("pk"),
                ).annotate(
                    popularities=popularities
                ).values("popularities")
            )

        feeds = self.queryset.annotate(
            profile_image=Concat(
                Value(settings.MEDIA_BUCKET_URL),
                F("user__profile__profile_image"),
                output_field=models.URLField()
            ),
            file=Case(
                When(
                    ~Q(files=""), then=JSONObject(
                        file_url=Concat(
                            Value(settings.MEDIA_BUCKET_URL),
                            F("files"),
                            output_field=models.URLField()
                        ),
                    )
                )
            ),
            profile_link=profile_link,
            current_user_action=current_user_action,
            popularities=post_remarks,
            current_user_commented=current_user_commented,
            total_comment=total_comment
        ).annotate(
            created=Now() - F("created_at"), created_=created_,
            updated=Now() - F("updated_at"), updated_=updated_
        ).values(
            "id", "user_id", "user__profile__username", "user__email",
            "profile_image", "text", "file", "profile_link", "popularities",
            "created_", "updated_", "current_user_action", "total_comment",
            "current_user_commented"
        )
        return Response(feeds, status=status.HTTP_200_OK)


class FeedsCreateAPIView(generics.CreateAPIView):
    serializer_class = FeedSerializer
    queryset = Feeds.objects.all()
    parser_classes = (parsers.MultiPartParser, )


class FeedsUpdateAPIView(generics.UpdateAPIView):
    serializer_class = FeedSerializer
    queryset = Feeds.objects.all()
    parser_classes = (parsers.MultiPartParser, )
    permission_classes = (IsOwner, )


class FeedsDeleteAPIView(generics.DestroyAPIView):
    serializer_class = FeedSerializer
    queryset = Feeds.objects.all()
    permission_classes = (IsOwner, )
