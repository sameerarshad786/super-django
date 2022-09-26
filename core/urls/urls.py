from django.urls import path, include

from .user_urls import USER_PATTERNS


urlpatterns = [
    path("user/", include(USER_PATTERNS))
]
