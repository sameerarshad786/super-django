from django.db.models import Q

from rest_framework import parsers, generics, status
from rest_framework.response import Response

from ..models import Posts
from ..serializers import Postserializer
from core.permissions import IsOwner
from ..service import post_popularities, user_commented, total_comment
from friendship.models import Follow


class PostsAPIView(generics.ListAPIView):
    serializer_class = Postserializer

    def get_queryset(self):
        followings = Follow.objects.filter(
            follower=self.request.user).values("followee_id")
        return Posts.objects.filter(
            Q(user=self.request.user) | Q(user_id__in=followings)
        ).order_by("-created_at")

    def get(self, request, *args, **kwargs):
        query = self.filter_queryset(self.get_queryset())
        query = post_popularities(query, request)
        query = user_commented(query, request)
        query = total_comment(query)
        serializer = self.get_serializer(
            query, context={"request": request}, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)


class PostsCreateAPIView(generics.CreateAPIView):
    serializer_class = Postserializer
    queryset = Posts.objects.all()
    parser_classes = (parsers.MultiPartParser, )


class PostsUpdateAPIView(generics.UpdateAPIView):
    serializer_class = Postserializer
    queryset = Posts.objects.all()
    parser_classes = (parsers.MultiPartParser, )
    permission_classes = (IsOwner, )


class PostsDeleteAPIView(generics.DestroyAPIView):
    serializer_class = Postserializer
    queryset = Posts.objects.all()
    permission_classes = (IsOwner, )
