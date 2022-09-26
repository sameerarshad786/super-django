from django.urls import path

from profiles import views

PROFILE_PATTERNS = [
    path("retrieve/", views.ProfileRetrieveAPIView.as_view(),
         name="profile-retrieve"),
    path("update/", views.ProfileUpdateAPIView.as_view(),
         name="profile-update")
]
