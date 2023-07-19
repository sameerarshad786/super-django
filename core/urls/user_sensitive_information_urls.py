from django.urls import path

from core import views


USER_SENSITIVE_INFORMATION_PATTERNS = [
    path("", views.UserSensitiveInformationAPIView.as_view(), name="sensitive-information")
]
