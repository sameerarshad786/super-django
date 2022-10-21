from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken


LOGIN_URL = reverse("login")


class PostTest(TestCase):
    def setUp(self) -> None:
        self.email = "testuser@paksocial.com"
        self.password = "testing321"
        self.user = User.objects.create(
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