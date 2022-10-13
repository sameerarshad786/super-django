from django.urls import path

from core import views


USER_AUTH_PATTERNS = [
    path("register/", views.RegisterAPIView.as_view(), name="register"),
    path("verify_email/", views.EmailVerificationAPIView.as_view(),
         name="verify-email"),
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("logout/", views.LogoutAPIView.as_view(), name="logout"),
    path(
        "password_reset/",
        views.ResetPasswordAPIView.as_view(),
        name="password-reset"
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        views.ResetPasswordConfirmAPIView.as_view(),
        name="password-reset-confirm"
    ),
    path(
        "password_reset_complete/",
        views.ResetPasswordCompleteAPIView.as_view(),
        name="password-reset-complete"
    )
]
