from django.urls import path

from profiles import views

PROFILE_PATTERNS = [
    path("detail/<str:username>/", views.ProfileRetrieveAPIView.as_view(),
         name="profile-retrieve"),
    path("update/<str:username>/", views.ProfileUpdateAPIView.as_view(),
         name="profile-update"),
    path("remove_profile_image/<str:username>/",
         views.DeleteProfileImageAPIView.as_view(),
         name="profile-image-delete"),
    path("remove_cover_image/<str:username>/",
         views.DeleteCoverImageAPIView.as_view(),
         name="cover-image-delete")
]
