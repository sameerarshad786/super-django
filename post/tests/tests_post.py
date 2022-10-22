from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken


LOGIN_URL = reverse("login")

POST_PATTERNS = reverse("post-create")


class PostTest(TestCase):
    def setUp(self) -> None:
        self.email = "testuser@paksocial.com"
        self.password = "testing321"
        self.user = get_user_model().objects.create(
            email=self.email
        )
        self.user.is_verified = True
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

    def test_user_create_post(self):
        payload = {
            "text": "post for testing api's"
        }
        response = self.client.post(
            POST_PATTERNS, payload,
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.access_token}"
        )
        self.assertEqual(response.status_code, 201)

    def test_user_update_post(self):
        payload = {
            "text": "post for testing api's"
        }
        res =  self.client.post(
            POST_PATTERNS, payload,
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.access_token}"
        )
        response = self.client.patch(
            reverse("post-update", args=[res.data.get("id")]),
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.access_token}"
        )
        self.assertEqual(response.status_code, 200)

    def test_user_delete_post(self):
        payload = {
            "text": "post for testing api's"
        }
        res =  self.client.post(
            POST_PATTERNS, payload,
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.access_token}"
        )
        response = self.client.delete(
            reverse("post-destroy", args=[res.data.get("id")]),
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.access_token}"
        )
        self.assertEqual(response.status_code, 204)

        response = self.client.post(
            POST_PATTERNS,
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.access_token}"
        )
        self.assertEqual(response.status_code, 201)

