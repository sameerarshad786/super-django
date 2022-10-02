from django.urls import path

from post import views


POST_PATTERNS = [
    path("reform/", views.PostAPIView.as_view(), name="post-create"),
    path("update/<str:pk>/", views.PostUpdateAPIView.as_view(),
         name="post-update"),
    path("destroy/<str:pk>/", views.PostDestroyAPIView.as_view(),
         name="post-destroy")
]

POST_REMARKS_PATTERNS = [
    path("create/", views.PostRemarkCreateAPIView.as_view(),
         name="remark-create"),
    path("update/<str:pk>/", views.PostRemarkUpdateAPIView.as_view(),
         name="remark-update"),
    path("destroy/<str:pk>/", views.PostRemarkDestroyAPIView.as_view(),
         name="remark-destroy")
]
