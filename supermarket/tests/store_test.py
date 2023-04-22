import json

from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

from profiles.models import Profile


LOGIN_URL = reverse("login")
CREATE_STORE = reverse("store-create")


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
        self.payload = {
            "user": self.user,
            "store_name": "my test store",
            "store_type": "testing",
            "location": json.dumps({
                "city": "karachi",
                "country": "pakistan"
            })
        }
        self.store = self.client.post(
            CREATE_STORE, self.payload, **self.auth_headers
        )

    def test_create_store(self):
        payload = {
            "user": self.user,
            "store_name": "django test store",
            "store_type": "testing",
            "location": json.dumps({
                "city": "karachi",
                "country": "pakistan"
            })
        }
        response = self.client.post(
            CREATE_STORE, payload, **self.auth_headers
        )
        self.assertEqual(response.status_code, 201)

    def test_update_store(self):
        response = self.client.patch(
            reverse("store-update", args=[self.store.data.get("id")]),
            self.payload,
            content_type='multipart/form-data; \
                boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_post(self):
        response = self.client.delete(
            reverse("store-delete", args=[self.store.data.get("id")]),
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 204)
