from django.urls import path

from packages.views import friend_views


FRIEND_URL = [
    path("send-request/",
         friend_views.SendFriendRequestAPIView.as_view(),
         name="send-friend-request"),
    path("all-requests/",
         friend_views.ListFriendRequestAPIView.as_view(),
         name="all-friend-request"),
    path("accept-requests/",
         friend_views.FriendRequestAcceptAPIView.as_view(),
         name="accept-request"),
    path("retrieve-send-request/<int:pk>/",
         friend_views.RetrieveFriendRequestAPIView.as_view(),
         name="retrieve-friend-request")
]
