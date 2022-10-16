from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

from core.models.user_model import User


REGISTER_URL = reverse("register")
VERIFY_EMAIL = reverse("verify-email")
LOGIN_URL = reverse("login")
LOGOUT_URL = reverse("logout")


class UserAuthenticationTest(TestCase):
    def setUp(self) -> None:
        self.email = "testuser2@paksocial.com"
        self.password = "testing321"
        self.confirm_password = "testing321"

    def test_create_user_with_no_matched_password_fields(self):
        payload = {
            "email": self.email,
            "password": self.password,
            "confirm_password": "testing3211"
        }
        response = self.client.post(
            REGISTER_URL, payload
        )
        self.assertEqual(response.status_code, 400)

    def test_create_user(self):
        payload = {
            "email": self.email,
            "password": self.password,
            "confirm_password": self.confirm_password
        }
        response = self.client.post(
            REGISTER_URL, payload
        )
        self.assertEqual(response.status_code, 201)

    def test_verify_user_with_valid_token(self):
        payload = {
            "email": self.email,
            "password": self.password,
            "confirm_password": self.confirm_password
        }
        self.client.post(
            REGISTER_URL, payload
        )
        user = get_user_model().objects.last()
        token = str(RefreshToken().for_user(user).access_token)
        res = self.client.get(
            VERIFY_EMAIL, {"token": token}
        )
        self.assertEqual(res.status_code, 200)

    def test_verify_user_with_invalid_token(self):
        payload = {
            "email": self.email,
            "password": self.password,
            "confirm_password": self.confirm_password
        }
        self.client.post(
            REGISTER_URL, payload
        )
        token_verification = {"token": "jkbnibuyhb09hq9bib8"}
        res = self.client.get(
            VERIFY_EMAIL, token_verification
        )
        self.assertEqual(res.status_code, 400)

    def test_user_login_failed_is_deactivate_by_admin(self):
        user = User.objects.create(
            email=self.email, is_verified=True, is_deactivate_by_admin=True
        )
        user.set_password(self.password)
        user.save()
        payload = {
            "email": self.email,
            "password": self.password
        }
        response = self.client.post(
            LOGIN_URL, payload
        )
        self.assertEqual(response.status_code, 401)

    def test_user_login_with_no_verification(self):
        user = User.objects.create(email=self.email)
        user.set_password(self.password)
        user.save()
        payload = {
            "email": self.email,
            "password": self.password
        }
        response = self.client.post(
            LOGIN_URL, payload
        )
        self.assertEqual(response.status_code, 401)

    def test_verified_user_login(self):
        user = User.objects.create(email=self.email, is_verified=True)
        user.set_password(self.password)
        user.save()
        payload = {
            "email": self.email,
            "password": self.password
        }
        response = self.client.post(
            LOGIN_URL, payload
        )
        self.assertEqual(response.status_code, 200)
