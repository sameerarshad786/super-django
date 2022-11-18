from rest_framework import generics, parsers, status
from rest_framework.response import Response

from profiles.serializers.profile_serializer import (
    ProfileSerializer, ProfileImageSerializer, CoverImageSerializer
)
from profiles.models.profile_model import Profile
from core.permissions import IsOwner
from ..location import get_location


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    lookup_field = "pk"

    def get(self, request, *args, **kwargs):
        data = dict()
        profile = Profile.objects.filter(id=kwargs["pk"])
        if profile:
            profile = Profile.objects.get(id=kwargs["pk"])
            location = get_location(request)
            data["id"] = profile.id
            data["user_id"] = profile.user.id
            data["username"] = profile.username
            data["email"] = profile.user.email
            data["gender"] = profile.gender
            data["profile_image"] = request.build_absolute_uri(
                profile.profile_image.url
            ) if profile.profile_image else None
            data["cover_image"] = request.build_absolute_uri(
                profile.cover_image.url
            ) if profile.cover_image else None
            data["phone_number"] = profile.phone_number
            data["about"] = profile.about
            data["skills"] = profile.skills
            data["education"] = profile.education
            data["current_status"] = profile.current_status
            data["address"] = location
            data["created"] = profile.created()
            data["updated"] = profile.updated()
            data["joined"] = profile.user.joined()
            data["user updated"] = profile.user.updated()
            if not profile.is_private or profile.user == request.user:
                return Response(data, status=status.HTTP_200_OK)
            return Response(
                {
                    "id": data["id"],
                    "user_id": data["user_id"],
                    "username": data["username"],
                    "message": "profile is private"
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {"message": "not found"}, status=status.HTTP_400_BAD_REQUEST
        )


class ProfileUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    parser_classes = (parsers.MultiPartParser, )
    permission_classes = (IsOwner, )
    queryset = Profile.objects.all()


class DeleteProfileImageAPIView(generics.UpdateAPIView):
    serializer_class = ProfileImageSerializer
    permission_classes = (IsOwner, )
    queryset = Profile.objects.all()


class DeleteCoverImageAPIView(generics.UpdateAPIView):
    serializer_class = CoverImageSerializer
    permission_classes = (IsOwner, )
    queryset = Profile.objects.all()
