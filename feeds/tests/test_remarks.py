from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework_simplejwt.tokens import RefreshToken

from profiles.models import Profile, Gender
from ..models import Popularity


CREATE_POSTS = reverse("feeds-create")
CREATE_REMARK = reverse("remarks-create")


class FeedTest(TestCase):
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
            user=self.user, username="test user",
            gender=Gender.MALE, profile_image="profile/male.png"
        )
        self.auth_headers = {
            'HTTP_AUTHORIZATION': f'Bearer {self.tokens.access_token}'
        }
        payload = {
            "text": "my first post"
        }
        self.post = self.client.post(
            CREATE_POSTS, payload, format="json",
            **self.auth_headers
        )

    def test_create_post_remark(self):
        payload = {
            "popularity": Popularity.HEART,
            "on_post": self.post.data.get("id")
        }
        response = self.client.post(
            CREATE_REMARK, payload, **self.auth_headers
        )
        self.assertEqual(response.status_code, 201)

    def test_update_post_remark(self):
        payload = {
            "popularity": Popularity.LIKE,
            "text": "my updatedt post"
        }
        response = self.client.patch(
            reverse("feeds-update", args=[self.post.data.get("id")]),
            payload, content_type='multipart/form-data; \
                boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_post_remark(self):
        response = self.client.delete(
            reverse("feeds-delete", args=[self.post.data.get("id")]),
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 204)
