from rest_framework import generics, parsers

from profiles.serializers.profile_serializer import (
    ProfileSerializer, ProfileImageSerializer, CoverImageSerializer
)
from profiles.models.profile_model import Profile
from core.permissions import IsOwner


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    lookup_field = "username"


class ProfileUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    parser_classes = (parsers.MultiPartParser, )
    permission_classes = (IsOwner, )
    queryset = Profile.objects.all()
    lookup_field = "username"


class DeleteProfileImageAPIView(generics.UpdateAPIView):
    serializer_class = ProfileImageSerializer
    permission_classes = (IsOwner, )
    queryset = Profile.objects.all()
    lookup_field = "username"


class DeleteCoverImageAPIView(generics.UpdateAPIView):
    serializer_class = CoverImageSerializer
    permission_classes = (IsOwner, )
    queryset = Profile.objects.all()
    lookup_field = "username"
