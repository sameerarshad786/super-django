from django_filters import rest_framework as filter

from friendship.models import FriendshipRequest


class FriendRequestFilter(filter.FilterSet):
    username = filter.CharFilter(field_name="from_user__profile__username", lookup_expr="iexact")

    class Meta:
        model = FriendshipRequest
        fields = ("id", "username", )
