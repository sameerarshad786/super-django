from django.urls import path

from profiles import views

PROFILE_PATTERNS = [
    path("", views.ProfileAPIView.as_view(),
         name="profile-view"),
    path("add_or_remove_profile_image/",
         views.DeleteProfileImageAPIView.as_view(),
         name="profile-image-delete"),
    path("add_or_remove_cover_image/",
         views.DeleteCoverImageAPIView.as_view(),
         name="cover-image-delete")
]
