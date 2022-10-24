from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

from profiles.models.profile_model import Profile


LOGIN_URL = reverse("login")

POST_URL = reverse("post-create")

REMARK_URL = reverse("remark-create")

COMMENT_URL = reverse("comment-create")


class MainSetup(TestCase):
    def setUp(self) -> None:
        """User TestCases"""
        self.email = "testuser@paksocial.com"
        self.password = "testing321"
        self.confirm_password = "testing321"
        self.user = get_user_model().objects.create_user(
            email=self.email, password=self.password
        )
        self.user.is_verified = True

        user_payload = {
            "email": self.email,
            "password": self.password
        }

        self.client.post(
            LOGIN_URL, user_payload
        )
        user = get_user_model().objects.last()
        self.tokens = RefreshToken().for_user(user)

        """Profile TestCase"""
        if self.user.is_verified:
            self.profile = Profile.objects.create(user=self.user)

        self.post = self.client.post(
            POST_URL, {"text": "my test post"},
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.access_token}"
        )
        self.post_id = self.post.data.get("id")
        cmnt_payload = {"comment": "nice keep it up", "on_post": self.post_id}
        self.comment = self.client.post(
            COMMENT_URL, cmnt_payload,
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.access_token}"
        )
        self.comment_id = self.comment.data.get("id")
