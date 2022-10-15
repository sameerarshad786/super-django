from django.urls import path

from profiles import views

PROFILE_PATTERNS = [
    path("detail/<uuid:pk>/", views.ProfileRetrieveAPIView.as_view(),
         name="profile-retrieve"),
    path("update/<uuid:pk>/", views.ProfileUpdateAPIView.as_view(),
         name="profile-update")
]
