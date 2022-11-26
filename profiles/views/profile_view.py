from django.db.models import F, Value, URLField
from django.db.models.functions import Concat
from django.conf import settings

from rest_framework import generics, parsers, status
from rest_framework.response import Response

from profiles.serializers.profile_serializer import (
    ProfileSerializer, ProfileImageSerializer, CoverImageSerializer
)
from profiles.models.profile_model import Profile
from core.permissions import IsOwner



class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.filter(id=kwargs["pk"]).annotate(
            profile_picture=Concat(
                Value(settings.MEDIA_BUCKET),
                F("profile_image"),
                output_field=URLField()
            ),
            cover_picture=Concat(
                Value(settings.MEDIA_BUCKET),
                F("cover_image"),
                output_field=URLField()
            ),
        ).values(
            "id", "user_id", "username", "user__email", "profile_picture",
            "cover_picture", "phone_number", "about", "skills", "education",
            "current_status", "employment_status", "profession", "location",
            "created_at", "updated_at"
        )
        return Response(profile, status=status.HTTP_200_OK)


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
