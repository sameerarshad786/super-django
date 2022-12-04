from django.urls import path, include

from .friendship_urls import FRIENDSHIP_URL


urlpatterns = [
    path("", include(FRIENDSHIP_URL)),
]
