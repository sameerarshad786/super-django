from rest_framework import generics, status
from rest_framework.response import Response

from ..serializers import FollowSerializer

from friendship.models import Follow


class GetAllFollowersAPIView(generics.ListAPIView):
    serializer_class = FollowSerializer

    def get_queryset(self):
        return Follow.objects.filter(
            followee=self.request.user
        ).order_by("-created")


class GetAllFollowingsAPIView(generics.ListAPIView):
    serializer_class = FollowSerializer

    def get_queryset(self):
        return Follow.objects.filter(
            follower=self.request.user
        ).order_by("-created")


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
