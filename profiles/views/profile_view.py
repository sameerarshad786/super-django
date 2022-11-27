from django.db.models import F, Value, Q, Case, When
from django.db.models.functions import Now, Concat, JSONObject
from django.db import models
from django.conf import settings

from rest_framework import generics, parsers, status
from rest_framework.response import Response

from profiles.serializers.profile_serializer import (
    ProfileSerializer, ProfileImageSerializer, CoverImageSerializer
)
from profiles.models.profile_model import Profile
from core.permissions import IsOwner
from core.tasks.timesince_calculations import created_, updated_


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.filter(id=kwargs["pk"]).select_related(
            "user"
        ).annotate(
            profile_picture=Concat(
                Value(settings.MEDIA_BUCKET_URL),
                F("profile_image"),
                output_field=models.URLField()
            ),
            cover_picture=Concat(
                Value(settings.MEDIA_BUCKET_URL),
                F("cover_image"),
                output_field=models.URLField()
            ),
        ).annotate(
            created=Now() - F("created_at"),
            updated=Now() - F("updated_at"),
            private_profile=Case(
                When(
                    Q(is_private=True) & ~Q(user=request.user),
                    then=JSONObject(
                        id=F("id"),
                        user_id=F("user_id"),
                        profile_picture=F("profile_picture"),
                        about=F("about"),
                        is_private=F("is_private"),
                    )
                ), output_field=models.JSONField()
            ),
            public_profile=Case(
                When(
                    Q(is_private=False) | Q(user=request.user),
                    then=JSONObject(
                        id=F("id"),
                        user_id=F("user_id"),
                        username=F("username"),
                        email=F("user__email"),
                        profile_picture=F("profile_picture"),
                        cover_picture=F("cover_picture"),
                        about=F("about"),
                        is_private=F("is_private"),
                        skills=F("skills"),
                        education=F("education"),
                        current_status=F("current_status"),
                        employment_status=F("employment_status"),
                        profession=F("profession"),
                        location=F("location"),
                        created=created_,
                        updated=updated_
                    )
                ), output_field=models.JSONField()
            )
        ).values("private_profile", "public_profile")
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
