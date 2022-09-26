from django.urls import path

from post import views


POST_PATTERNS = [
    path("reform/", views.PostAPIView.as_view(), name="post-create"),
    path("update/<str:pk>/", views.PostUpdateAPIView.as_view(), name="post-update"),
    path("destroy/<str:pk>/", views.PostDestroyAPIView.as_view(), name="post-destroy")
]
