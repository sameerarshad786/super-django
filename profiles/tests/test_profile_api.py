from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

from ..models import Profile
from core.utils.temp_image import temporary_image


LOGIN_URL = reverse("login")


class UserProfileTest(TestCase):
    def setUp(self) -> None:
        self.email = "testuser@paksocial.com"
        self.password = "testing321"
        self.confirm_password = "testing321"
        self.user = get_user_model().objects.create_user(
            email=self.email, password=self.password
        )
        self.user.is_verified = True
        user = get_user_model().objects.last()
        self.tokens = RefreshToken().for_user(user)
        self.profile = Profile.objects.create(
            user=self.user, username="test user"
        )
        self.auth_headers = {
            'HTTP_AUTHORIZATION': f'Bearer {self.tokens.access_token}'
        }

    def test_retrieve_profile(self):
        response = self.client.get(
            reverse("profile-retrieve", args=[self.profile.username]),
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)

    def test_update_verified_user_profile(self):
        payload = {
            "username": "test user"
        }
        response = self.client.patch(
            reverse("profile-update", args=[self.profile.username]),
            payload, content_type='multipart/form-data; \
                boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)

    def test_update_someone_profile_failed(self):
        response = self.client.patch(
            reverse(
                "profile-update",
                args=["random"]
            ),
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 404)

    def test_update_profile_and_cover_image(self):
        payload = {
            "profile_image": temporary_image(),
            "cover_image": temporary_image()
        }
        response = self.client.patch(
            reverse(
                "profile-update", args=[self.profile.username]
            ),
            payload, content_type='multipart/form-data; \
                boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
