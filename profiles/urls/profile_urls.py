from django.urls import path

from profiles import views

PROFILE_PATTERNS = [
    path("", views.ProfileAPIView.as_view(),
         name="profile-view"),
    path("remove_profile_image/",
         views.DeleteProfileImageAPIView.as_view(),
         name="profile-image-delete"),
    path("remove_cover_image/",
         views.DeleteCoverImageAPIView.as_view(),
         name="cover-image-delete")
]
