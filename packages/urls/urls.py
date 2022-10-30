from django.urls import path, include

from .friend_urls import FRIEND_URL


urlpatterns = [
    path("friend/", include(FRIEND_URL))
]
