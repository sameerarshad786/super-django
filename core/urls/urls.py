from django.urls import path, include

from .user_urls import USER_AUTH_PATTERNS
from .user_sensitive_information_urls import USER_SENSITIVE_INFORMATION_PATTERN


urlpatterns = [
    path("user/", include(USER_AUTH_PATTERNS)),
    path(
        "sensitive-information/", include(USER_SENSITIVE_INFORMATION_PATTERN)
    )
]
