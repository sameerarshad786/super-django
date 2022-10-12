from django.urls import path

from core import views


USER_AUTH_PATTERNS = [
    path("register/", views.RegisterAPIView.as_view(), name="register"),
    path("verify_email/", views.EmailVerificationAPIView.as_view(),
         name="verify-email"),
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("logout/", views.LogoutAPIView.as_view(), name="logout"),
]
