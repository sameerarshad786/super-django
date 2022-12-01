from django.db.models import Subquery, OuterRef, F, Count
from django.db.models.functions import JSONObject, Now
from django.contrib.postgres.aggregates import ArrayAgg

from rest_framework import parsers, generics, status
from rest_framework.response import Response

from ..models import Feeds, Comments, Remarks
from ..serializers import CommentSerializer
from core.permissions import IsOwner
from ..tasks.querysets import (
    profile_link, profile_picture, popularities, created_, updated_
)


class PostCommentsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        replies_count = Subquery(Comments.objects.filter(
            on_comment=OuterRef("pk")
        ).values("on_comment").annotate(count=Count("pk")).values("count"))
        comment_remarks = Subquery(Remarks.objects.filter(
            on_comment=OuterRef("pk")
        ).values("on_comment").annotate(count=Count("pk")).annotate(
            popularities=popularities
        ).values("popularities"))

        # https://stackoverflow.com/questions/63020407/return-multiple-values-in-subquery-in-django-orm
        replies = Subquery(Comments.objects.filter(
            on_comment=OuterRef("pk")
        ).values("on_comment", "created_at", "updated_at").annotate(
            created=Now() - F("created_at"), created_=created_,
            updated=Now() - F("updated_at"), updated_=updated_
        ).annotate(
            details=ArrayAgg(
                JSONObject(
                    id="id",
                    user_id="user_id",
                    username="user__profile__username",
                    text="text",
                    files="files",
                    created="created_",
                    updated="updated_",
                    profile_link=profile_link,
                    profile_image=profile_picture,
                    comment_remarks=comment_remarks,
                    replies_count=replies_count
                )
            )
        ).values("details"))

        comment = Subquery(Comments.objects.filter(
            on_post=OuterRef("pk"), on_comment=None
        ).values("on_post", "created_at", "updated_at").annotate(
            created=Now() - F("created_at"), created_=created_,
            updated=Now() - F("updated_at"), updated_=updated_
        ).values("created_").annotate(
            details=ArrayAgg(
                JSONObject(
                    id="id",
                    user_id="user_id",
                    username="user__profile__username",
                    text="text",
                    files="files",
                    created="created_",
                    updated="updated_",
                    profile_link=profile_link,
                    profile_image=profile_picture,
                    comment_remarks=comment_remarks,
                    comment_replies=replies
                )
            )
        ).values("details"))

        post = Feeds.objects.filter(id=kwargs["on_post_id"]).annotate(
            comment=comment,
        ).values("comment")
        return Response(post, status=status.HTTP_200_OK)


class OnCommentsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CommentSerializer
    queryset = Comments.objects.all()

    def get(self, request, *args, **kwargs):
        replies_count = Subquery(Comments.objects.filter(
            on_comment=OuterRef("pk")
        ).values("on_comment").annotate(count=Count("pk")).values("count"))
        comment_remarks = Subquery(Remarks.objects.filter(
            on_comment=OuterRef("pk")
        ).values("on_comment").annotate(count=Count("pk")).annotate(
            popularities=popularities
        ).values("popularities"))

        # https://stackoverflow.com/questions/63020407/return-multiple-values-in-subquery-in-django-orm
        replies = Subquery(Comments.objects.filter(
            on_comment=OuterRef("pk")
        ).values("on_comment", "created_at", "updated_at").annotate(
            created=Now() - F("created_at"), created_=created_,
            updated=Now() - F("updated_at"), updated_=updated_
        ).annotate(
            details=ArrayAgg(
                JSONObject(
                    id="id",
                    user_id="user_id",
                    username="user__profile__username",
                    text="text",
                    files="files",
                    created="created_",
                    updated="updated_",
                    profile_link=profile_link,
                    profile_image=profile_picture,
                    comment_remarks=comment_remarks,
                    replies_count=replies_count
                )
            )
        ).values("details"))

        comment = Comments.objects.filter(on_comment=kwargs["pk"]).annotate(
            created=Now() - F("created_at"), created_=created_,
            updated=Now() - F("updated_at"), updated_=updated_
        ).values("created_").annotate(
            details=ArrayAgg(
                JSONObject(
                    id="id",
                    user_id="user_id",
                    username="user__profile__username",
                    text="text",
                    files="files",
                    created="created_",
                    updated="updated_",
                    profile_link=profile_link,
                    profile_image=profile_picture,
                    comment_remarks=comment_remarks,
                    comment_replies=replies
                )
            )
        ).values("details")
        return Response(comment)


class CommentsCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comments.objects.all()
    parser_classes = (parsers.MultiPartParser, )


class CommentsUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CommentSerializer
    queryset = Comments.objects.all()
    parser_classes = (parsers.MultiPartParser, )
    permission_classes = (IsOwner, )


class CommentsDeleteAPIView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comments.objects.all()
    permission_classes = (IsOwner, )
