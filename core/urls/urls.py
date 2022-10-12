from django.urls import path, include

from .user_urls import USER_AUTH_PATTERNS


urlpatterns = [
    path("user/", include(USER_AUTH_PATTERNS))
]
