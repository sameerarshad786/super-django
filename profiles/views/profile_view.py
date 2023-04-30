from rest_framework import generics, status, parsers
from rest_framework.response import Response
from rest_framework.decorators import permission_classes

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from profiles.serializers.profile_serializer import (
    ProfileSerializer, ProfileImageSerializer, CoverImageSerializer
)
from profiles.models.profile_model import Profile
from core.permissions import IsOwner


class ProfileAPIView(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    parser_classes = (parsers.MultiPartParser, )

    username_param_config = openapi.Parameter(
        "username",
        in_=openapi.IN_QUERY,
        description="filter by username, if username is not provided then current user profile will be displayed",
        type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[username_param_config])
    def get(self, request, *args, **kwargs):
        username = self.request.GET.get("username")
        try:
            if username:
                profile = Profile.objects.get(username=username)
            else:
                profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response(
                {"message": "No profile exists with this username"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(instance=profile).data
        return Response(serializer, status=status.HTTP_200_OK)

    @permission_classes([IsOwner])
    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user.profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteProfileImageAPIView(generics.GenericAPIView):
    serializer_class = ProfileImageSerializer
    queryset = Profile.objects.all()
    permission_classes = (IsOwner, )
    parser_classes = (parsers.MultiPartParser, )

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user.profile, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteCoverImageAPIView(generics.GenericAPIView):
    serializer_class = CoverImageSerializer
    queryset = Profile.objects.all()
    permission_classes = (IsOwner, )
    parser_classes = (parsers.MultiPartParser, )

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user.profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
