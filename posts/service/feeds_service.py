import json

from typing import Union

from django.db.models import (
    Q, F, Count, OuterRef, Subquery, Exists, Value, Func
)
from django.db.models.functions import JSONObject, Coalesce
from django.contrib.postgres.aggregates import BoolOr
from django.db import models
from django.db.models import Prefetch

from ..models import Posts, Comments, Remarks


def post_popularities(query: Union[Posts, None], user):
    post_remarks = Remarks.objects.filter(
            post=OuterRef("pk"), comment=None
        ).only("post").annotate(
            # https://docs.djangoproject.com/en/4.2/ref/models/conditional-expressions/#conditional-aggregation
            popularities=JSONObject(
                total_actions=Count("pk"),
                like=Count("pk", filter=Q(like=True)),
                heart=Count("pk", filter=Q(heart=True)),
                funny=Count("pk", filter=Q(funny=True)),
                insightful=Count("pk", filter=Q(insightful=True)),
                disappoint=Count("pk", filter=Q(disappoint=True)),
                current_user_like=BoolOr(Q(user=user, like=True)),
                current_user_heart=BoolOr(Q(user=user, heart=True)),
                current_user_funny=BoolOr(Q(user=user, funny=True)),
                current_user_insightful=BoolOr(Q(user=user, insightful=True)),
                current_user_disappoint=BoolOr(Q(user=user, disappoint=True)),
            )
        ).values("popularities")
    return query.annotate(
        # https://stackoverflow.com/questions/72072872/django-get-max-length-value-from-same-model-with-coalesce
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


def comment_popularities(query: Union[Comments, None], user):
    comment_popularities = Remarks.objects.filter(
            comment=OuterRef("pk")
        ).only("comment").annotate(
            popularities=JSONObject(
                total_actions=Count("pk"),
                like=Count("pk", filter=Q(like=True)),
                heart=Count("pk", filter=Q(heart=True)),
                funny=Count("pk", filter=Q(funny=True)),
                insightful=Count("pk", filter=Q(insightful=True)),
                disappoint=Count("pk", filter=Q(disappoint=True)),
                current_user_like=BoolOr(Q(user=user, like=True)),
                current_user_heart=BoolOr(Q(user=user, heart=True)),
                current_user_funny=BoolOr(Q(user=user, funny=True)),
                current_user_insightful=BoolOr(Q(user=user, insightful=True)),
                current_user_disappoint=BoolOr(Q(user=user, disappoint=True)),
            )
        ).values("popularities")
    return query.annotate(
        # https://stackoverflow.com/questions/72072872/django-get-max-length-value-from-same-model-with-coalesce
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


def total_comment(query: Union[Posts, None]):
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


def user_commented(query, user):
    current_user_commented = Comments.objects.filter(
        post=OuterRef("pk"), user=user)
    return query.annotate(
        current_user_commented=Exists(current_user_commented)
    )


def user_replied(query, user):
    user_replied = Comments.objects.filter(
        parent=OuterRef("pk"), user=user)
    return query.annotate(
        user_replied=Exists(user_replied)
    )
