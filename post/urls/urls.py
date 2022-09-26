from django.urls import path, include

from .post_url import POST_PATTERNS


urlpatterns = [
    path("feed/", include(POST_PATTERNS))
]
