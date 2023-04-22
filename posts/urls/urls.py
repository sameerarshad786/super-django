from django.urls import path, include

from ..views import posts_view, comments_view, remarks_view


POSTS_PATTERNS = [
    path("", posts_view.PostsAPIView.as_view(), name="posts-list"),
    path(
        "create/", posts_view.PostsCreateAPIView.as_view(),
        name="posts-create"
    ),
    path(
        "update/<str:pk>/", posts_view.PostsUpdateAPIView.as_view(),
        name="posts-update"
    ),
    path(
        "delete/<str:pk>/", posts_view.PostsDeleteAPIView.as_view(),
        name="posts-delete"
    )
]

COMMENTS_PATTERNS = [
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


REMARKS_PATTERNS = [
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
    path("post/", include(POSTS_PATTERNS)),
    path("comments/", include(COMMENTS_PATTERNS)),
    path("remarks/", include(REMARKS_PATTERNS))
]
