from django.urls import path

from ..views import store_views


STORE_URLS = [
    path(
        "create/", store_views.StoreCreateAPIView.as_view(),
        name="store-create"
    ),
    path(
        "detail/<str:name>/", store_views.StoreRetrieveAPIView.as_view(),
        name="store-retrieve"
    ),
    path(
        "update/<str:pk>/", store_views.StoreUpdateAPIView.as_view(),
        name="store-update"
    ),
    path(
        "delete/<str:pk>/", store_views.StoreDestroyAPIView.as_view(),
        name="store-delete"
    )
]
