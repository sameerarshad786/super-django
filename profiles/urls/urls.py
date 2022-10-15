from django.urls import path, include

from .profile_urls import PROFILE_PATTERNS

urlpatterns = [
    path("", include(PROFILE_PATTERNS))
]
