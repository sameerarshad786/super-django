from django.urls import path

from packages.views import friend_views


FRIEND_URL = [
    path("send-request/",
         friend_views.SendFriendRequestAPIView.as_view(),
         name="send-friend-request"),
    path("all-requests/",
         friend_views.ListFriendRequestAPIView.as_view(),
         name="all-friend-request"),
    path("requests-action/",
         friend_views.AcceptFriendRequestAPIView.as_view(),
         name="accept-request"),
    path("all-friends/",
         friend_views.AllFriendListAPIView.as_view(),
         name="all-friends"),
]
