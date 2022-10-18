from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

from core.models.user_model import User
from profiles.models.profile_model import Profile


LOGIN_URL = reverse("login")


class UserProfileTest(TestCase):
    def setUp(self) -> None:
        self.email = "testuser@paksocial.com"
        self.password = "testing321"
        self.user = User.objects.create(
            email=self.email, is_verified=True
        )
        self.user.set_password(self.password)
        self.user.save()

        user_payload = {
            "email": self.email,
            "password": self.password
        }

        self.client.post(
            LOGIN_URL, user_payload
        )
        user = get_user_model().objects.last()
        self.tokens = RefreshToken().for_user(user)

    def test_verified_user_profile(self):
        self.assertTrue(self.user.is_verified)
        profile = Profile.objects.create(user=self.user)
        self.assertTrue(profile)

    def test_retrieve_profile(self):
        self.assertTrue(self.user.is_verified)
        profile = Profile.objects.create(user=self.user)
        self.assertTrue(profile)

        response = self.client.get(
            reverse("profile-retrieve", args=[profile.id]),
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.access_token}"
        )
        self.assertEqual(response.status_code, 200)
