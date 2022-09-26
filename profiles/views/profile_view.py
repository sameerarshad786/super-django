from rest_framework import generics, permissions, parsers

from profiles.serializers.profile_serializer import ProfileSerializer
from profiles.models.profile_model import Profile


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Profile.objects.all()


class ProfileUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated, )
    parser_classes = (parsers.MultiPartParser, )
    queryset = Profile.objects.all()
