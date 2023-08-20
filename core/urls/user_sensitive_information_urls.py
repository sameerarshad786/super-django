from django.urls import path

from core import views


USER_SENSITIVE_INFORMATION_PATTERN = [
    path(
        "",
        views.UserSensitiveInformationAPIView.as_view(),
        name="sensitive-information"
    )
]
