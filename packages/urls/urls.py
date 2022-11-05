from django.urls import path, include

from .friendship_urls import FRIENDSHIP_URL


urlpatterns = [
    path("friendship/", include(FRIENDSHIP_URL)),
]
