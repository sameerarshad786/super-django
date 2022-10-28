from django.urls import path, include

from .post_url import (
    POST_PATTERNS, POST_REMARKS_PATTERNS, COMMENT_REMARKS_PATTERNS,
    COMMENTS_PATTERNS
)


urlpatterns = [
    path("feed/", include(POST_PATTERNS)),
    path("post-remarks/", include(POST_REMARKS_PATTERNS)),
    path("comment-remarks/", include(COMMENT_REMARKS_PATTERNS)),
    path("comment/", include(COMMENTS_PATTERNS))
]
