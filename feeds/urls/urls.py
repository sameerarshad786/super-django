from django.urls import path, include

from ..views import feeds_view, comments_view, remarks_view


FEEDS_API_VIEW = [
    path("", feeds_view.FeedsAPIView.as_view(), name="feeds-list"),
    path(
        "create/", feeds_view.FeedsCreateAPIView.as_view(),
        name="feeds-create"
    ),
    path(
        "update/<str:pk>/", feeds_view.FeedsUpdateAPIView.as_view(),
        name="feeds-update"
    ),
    path(
        "delete/<str:pk>/", feeds_view.FeedsDeleteAPIView.as_view(),
        name="feeds-delete"
    )
]

COMMENTS_API_VIEW = [
    path(
        "detail/<uuid:post_id>/",
        comments_view.CommentsRetrieveAPIView.as_view(),
        name="post-comments-retrieve"
    ),
    path(
        "comments-replies/<str:pk>/",
        comments_view.ChildCommentsRetrieveAPIView.as_view(),
        name="comments-retrieve"
    ),
    path(
        "create/", comments_view.CommentsCreateAPIView.as_view(),
        name="comments-create"
    ),
    path(
        "update/<str:pk>/", comments_view.CommentsUpdateAPIView.as_view(),
        name="comments-update"
    ),
    path(
        "delete/<str:pk>/", comments_view.CommentsDeleteAPIView.as_view(),
        name="comments-delete"
    )
]


REMARKS_API_VIEW = [
    path(
        "post-remarks/<uuid:post_id>",
        remarks_view.PostRemarksRetrieveAPIView.as_view(),
        name="post-remarks"
    ),
    path(
        "comment-remarks/<uuid:comment_id>",
        remarks_view.CommentRemarksRetrieveAPIView.as_view(),
        name="comment-remarks"
    ),
    path(
        "create/", remarks_view.RemarksCreateAPIView.as_view(),
        name="remarks-create"
    ),
    path(
        "update/<str:pk>/", remarks_view.RemarksUpdateAPIView.as_view(),
        name="remarks-update"
    ),
    path(
        "delete/<str:pk>/", remarks_view.RemarksDeleteAPIView.as_view(),
        name="remarks-delete"
    )
]


urlpatterns = [
    path("post/", include(FEEDS_API_VIEW)),
    path("comments/", include(COMMENTS_API_VIEW)),
    path("remarks/", include(REMARKS_API_VIEW))
]
