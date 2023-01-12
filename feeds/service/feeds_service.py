from django.db.models import (
    Count, OuterRef, Subquery, Exists, Q
)
from django.db.models.functions import JSONObject

from ..models import Remarks, Comments, Popularity
from ..service.custom_db_func import CustomBoolOr


def feed_popularities(query, request):
    post_remarks = Remarks.objects.filter(
        post=OuterRef("pk"), comment=None).values("post").annotate(
        popularities=JSONObject(
            total_actions=Count("pk"),
            like=Count("pk", filter=Q(popularity=Popularity.LIKE)),
            heart=Count("pk", filter=Q(popularity=Popularity.HEART)),
            funny=Count("pk", filter=Q(popularity=Popularity.FUNNY)),
            insightful=Count(
                "pk", filter=Q(popularity=Popularity.INSIGHTFUL)),
            disappoint=Count(
                "pk", filter=Q(popularity=Popularity.DISAPPOINT)),
            current_user_like=CustomBoolOr(
                Q(user=request.user, popularity=Popularity.LIKE)
            ),
            current_user_heart=CustomBoolOr(
                Q(user=request.user, popularity=Popularity.HEART)
            ),
            current_user_funny=CustomBoolOr(
                Q(user=request.user, popularity=Popularity.FUNNY)
            ),
            current_user_insightful=CustomBoolOr(
                Q(user=request.user, popularity=Popularity.INSIGHTFUL)
            ),
            current_user_disappoint=CustomBoolOr(
                Q(user=request.user, popularity=Popularity.DISAPPOINT)
            )
        )
    ).values("popularities")
    return query.annotate(
        popularities=Subquery(post_remarks),
    )


def comment_popularities(query, request):
    post_remarks = Remarks.objects.filter(
        comment=OuterRef("pk")).values("post").annotate(
        popularities=JSONObject(
            total_actions=Count("pk"),
            like=Count("pk", filter=Q(popularity=Popularity.LIKE)),
            heart=Count("pk", filter=Q(popularity=Popularity.HEART)),
            funny=Count("pk", filter=Q(popularity=Popularity.FUNNY)),
            insightful=Count(
                "pk", filter=Q(popularity=Popularity.INSIGHTFUL)),
            disappoint=Count(
                "pk", filter=Q(popularity=Popularity.DISAPPOINT)),
            current_user_like=CustomBoolOr(
                Q(user=request.user, popularity=Popularity.LIKE)
            ),
            current_user_heart=CustomBoolOr(
                Q(user=request.user, popularity=Popularity.HEART)
            ),
            current_user_funny=CustomBoolOr(
                Q(user=request.user, popularity=Popularity.FUNNY)
            ),
            current_user_insightful=CustomBoolOr(
                Q(user=request.user, popularity=Popularity.INSIGHTFUL)
            ),
            current_user_disappoint=CustomBoolOr(
                Q(user=request.user, popularity=Popularity.DISAPPOINT)
            )
        )
    ).values("popularities")
    return query.annotate(
        popularities=Subquery(post_remarks),
    )


def total_comment(query):
    total_comment = Comments.objects.filter(
        post=OuterRef("pk")).values("post").annotate(
            total_comment=Count("pk")
        ).values("total_comment")
    return query.annotate(
        total_comment=Subquery(total_comment)
    )


def total_replies(query):
    total_replies = Comments.objects.filter(
        comment=OuterRef("pk")).values("comment").annotate(
            total_replies=Count("pk")
        ).values("total_replies")
    return query.annotate(
        total_replies=Subquery(total_replies)
    )


def user_commented(query, request):
    current_user_commented = Comments.objects.filter(
        post=OuterRef("pk"), user=request.user)
    return query.annotate(
        current_user_commented=Exists(current_user_commented)
    )


def user_replied(query, request):
    user_replied = Comments.objects.filter(
        comment=OuterRef("pk"), user=request.user)
    return query.annotate(
        user_replied=Exists(user_replied)
    )
