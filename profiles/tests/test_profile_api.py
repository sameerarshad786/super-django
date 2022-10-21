from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

from profiles.models.profile_model import Profile


LOGIN_URL = reverse("login")


class UserProfileTest(TestCase):
    def setUp(self) -> None:
        self.email = "testuser@paksocial.com"
        self.password = "testing321"
        self.user = get_user_model().objects.create(
            email=self.email
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

    def test_create_verified_user_profile(self):
        self.user.is_verified = True
        self.assertTrue(self.user.is_verified)
        profile = Profile.objects.create(user=self.user)
        self.assertTrue(profile)

    def test_retrieve_profile(self):
        self.user.is_verified = True
        self.assertTrue(self.user.is_verified)
        profile = Profile.objects.create(user=self.user)
        self.assertTrue(profile)

        response = self.client.get(
            reverse("profile-retrieve", args=[profile.id]),
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.access_token}"
        )
        self.assertEqual(response.status_code, 200)

    def test_update_verified_user_profile(self):
        self.user.is_verified = True
        self.assertTrue(self.user.is_verified)
        profile = Profile.objects.create(user=self.user)
        self.assertTrue(profile)

        response = self.client.patch(
            reverse("profile-update", args=[profile.id]),
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.access_token}"
        )
        self.assertEqual(response.status_code, 200)

    def test_update_someone_profile_failed(self):
        self.user.is_verified = True
        self.assertTrue(self.user.is_verified)
        profile = Profile.objects.create(user=self.user)
        self.assertTrue(profile)

        response = self.client.patch(
            reverse("profile-update",
                    args=["0db2ad5c-cca2-47e1-a1b1-3ba0d006023a"]),
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.access_token}"
        )
        self.assertEqual(response.status_code, 404)
