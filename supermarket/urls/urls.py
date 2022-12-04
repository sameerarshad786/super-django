from django.urls import path, include

from .store_urls import STORE_URLS


urlpatterns = [
    path("store/", include(STORE_URLS))
]
