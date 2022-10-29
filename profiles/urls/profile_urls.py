from django.urls import path

from profiles import views

PROFILE_PATTERNS = [
    path("detail/<uuid:pk>/", views.ProfileRetrieveAPIView.as_view(),
         name="profile-retrieve"),
    path("update/<uuid:pk>/", views.ProfileUpdateAPIView.as_view(),
         name="profile-update"),
    path("remove_profile_image/<uuid:pk>/",
         views.DeleteProfileImageAPIView.as_view(),
         name="profile-image-delete"),
    path("remove_cover_image/<uuid:pk>/",
         views.DeleteCoverImageAPIView.as_view(),
         name="cover-image-delete")
]
