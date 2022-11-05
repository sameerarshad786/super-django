from rest_framework import generics, status
from rest_framework.response import Response

from ..serializers import FollowSerializer
from ..utils import get_timesince

from friendship.models import Follow


class GetAllFollowersAPIView(generics.ListAPIView):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()

    def get(self, request, *args, **kwargs):
        followers = Follow.objects.filter(followee=self.request.user)
        result = []
        for follower in followers:
            result.append({
                "id": follower.id,
                "user_id": follower.follower.id,
                "username": follower.follower.profile.username,
                "profile_image": request.build_absolute_uri(
                    follower.follower.profile.profile_image.url),
                "followed": get_timesince(follower.created),
            })
        return Response(result)


class GetAllFollowingsAPIView(generics.ListAPIView):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()

    def get(self, request, *args, **kwargs):
        followings = Follow.objects.filter(follower=self.request.user)
        result = []
        for following in followings:
            result.append({
                "id": following.id,
                "user_id": following.followee.id,
                "username": following.followee.profile.username,
                "profile_image": request.build_absolute_uri(
                    following.followee.profile.profile_image.url),
                "followed": get_timesince(following.created)
            })
        return Response(result, status=status.HTTP_200_OK)


class FollowUserAPIView(generics.CreateAPIView):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()


class UnFollowUserAPIView(generics.DestroyAPIView):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()

    def destroy(self, request, *args, **kwargs):
        followee = Follow.objects.filter(
            followee=kwargs["followee_id"], follower=request.user
        )
        if followee.exists():
            followee.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {"message": "you cant follow this user"},
            status=status.HTTP_400_BAD_REQUEST
        )
