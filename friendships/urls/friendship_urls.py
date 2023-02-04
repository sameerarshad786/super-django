from django.urls import path

from friendships.views import friend_view, follow_view, block_view


FRIENDSHIP_URL = [
    # friend request and accept API's
    path("send-request/",
         friend_view.SendFriendRequestAPIView.as_view(),
         name="send-friend-request"),
    path("recieved-requests/",
         friend_view.RecievedRequestAPIView.as_view(),
         name="all-friend-requests"),
    path("sent-requests/",
         friend_view.SentRequestsAPIView.as_view(),
         name="sent-friend-requests"),
    path("accept-request/",
         friend_view.AcceptFriendRequestAPIView.as_view(),
         name="accept-request"),
    path("cancel-request/<int:user_id>/",
         friend_view.CancelFriendRequestAPIView.as_view(),
         name="cancel-request"),
    path("friends/<int:user_id>",
         friend_view.FriendListAPIView.as_view(),
         name="all-friends"),
    path("unfriend/<int:user_id>/",
         friend_view.UnFriendAPIView.as_view(),
         name="all-friends"),

    # follow and unfollow users API's
    path("followers/<int:user_id>", follow_view.FollowersAPIView.as_view(),
         name="all-followers"),
    path("followings/<int:user_id>", follow_view.FollowingsAPIView.as_view(),
         name="all-followings"),
    path("follow/", follow_view.FollowUserAPIView.as_view(),
         name="follow"),
    path("unfollow/<int:user_id>/",
         follow_view.UnFollowUserAPIView.as_view(),
         name="unfollow"),

    # block and unblock users API's
    path("block-list/", block_view.BlockedListAPIView.as_view(),
         name="block-list"),
    path("block/", block_view.BlockUserAPIView.as_view(),
         name="block"),
    path("unblock/<int:user_id>/", block_view.UnBlockUserAPIView.as_view(),
         name="unblock")
]
