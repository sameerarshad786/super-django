import json

from django.db.models import (
    Q, F, Count, OuterRef, Subquery, Exists, Value, Func
)
from django.db.models.functions import JSONObject, Coalesce
from django.db import models

from ..models import Remarks, Comments
from ..service.custom_db_func import CustomBoolOr


def post_popularities(query, request):
    post_remarks = Remarks.objects.filter(
        post=OuterRef("pk"), comment=None).values("post").annotate(
            popularities=JSONObject(
                total_actions=Count("pk"),
                like=Count(
                    "pk", filter=Q(popularity=Remarks.Popularity.LIKE)),
                heart=Count(
                    "pk", filter=Q(popularity=Remarks.Popularity.HEART)),
                funny=Count(
                    "pk", filter=Q(popularity=Remarks.Popularity.FUNNY)),
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
                )
            )
        ).values("popularities")
    return query.annotate(
        popularities=Coalesce(Subquery(post_remarks), Value(
            json.dumps(
                {
                    "like": 0,
                    "funny": 0,
                    "heart": 0,
                    "disappoint": 0,
                    "insightful": 0,
                    "total_actions": 0,
                    "current_user_like": False,
                    "current_user_funny": False,
                    "current_user_heart": False,
                    "current_user_disappoint": False,
                    "current_user_insightful": False
                }
            )
        ), output_field=models.JSONField())
    )


def comment_popularities(query, request):
    comment_popularities = Remarks.objects.filter(
        comment=OuterRef("pk")).values("comment").annotate(
            popularities=JSONObject(
                total_actions=Count("pk"),
                like=Count(
                    "pk", filter=Q(popularity=Remarks.Popularity.LIKE)),
                heart=Count(
                    "pk", filter=Q(popularity=Remarks.Popularity.HEART)),
                funny=Count(
                    "pk", filter=Q(popularity=Remarks.Popularity.FUNNY)),
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
                )
            )
        ).values("popularities")
    return query.annotate(
        comment_popularities=Coalesce(Subquery(comment_popularities), Value(
            json.dumps(
                {
                    "like": 0,
                    "funny": 0,
                    "heart": 0,
                    "disappoint": 0,
                    "insightful": 0,
                    "total_actions": 0,
                    "current_user_like": False,
                    "current_user_funny": False,
                    "current_user_heart": False,
                    "current_user_disappoint": False,
                    "current_user_insightful": False
                }
            )
        ), output_field=models.JSONField())
    )


def total_comment(query):
    total_comment = Comments.objects.filter(
        post=OuterRef("pk")).values("post").annotate(
            total_comment=Func(F("pk"), function="COUNT")
        ).values("total_comment")
    return query.annotate(
        total_comment=Subquery(total_comment)
    )


def total_replies(query):
    total_replies = Comments.objects.filter(
        parent=OuterRef("pk")).values("parent").annotate(
            total_replies=Func(F("pk"), function="COUNT")
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
        parent=OuterRef("pk"), user=request.user)
    return query.annotate(
        user_replied=Exists(user_replied)
    )
