from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes, smart_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework_simplejwt.tokens import RefreshToken

from core.models.user_model import User


REGISTER_URL = reverse("register")
VERIFY_EMAIL = reverse("verify-email")
LOGIN_URL = reverse("login")
LOGOUT_URL = reverse("logout")
PASSWORD_RESET = reverse("password-reset")
PASSWORD_RESET_COMPLETE = reverse("password-reset-complete")


class UserAuthenticationTest(TestCase):
    def setUp(self) -> None:
        self.email = "testuser@paksocial.com"
        self.password = "testing321"
        self.confirm_password = "testing321"
        self.user = User.objects.create(
            email=self.email
        )
        self.user.set_password(self.password)
        self.user.save()

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
            "email": "testuser2@paksocial.com",
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
        payload = {"token": token}
        res = self.client.get(
            VERIFY_EMAIL, payload
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
        self.user.is_verified = True
        self.user.is_deactivate_by_admin = True
        self.user.save()
        payload = {
            "email": self.email,
            "password": self.password
        }
        response = self.client.post(
            LOGIN_URL, payload
        )
        self.assertEqual(response.status_code, 401)

    def test_user_login_with_no_verification(self):
        payload = {
            "email": self.email,
            "password": self.password
        }
        response = self.client.post(
            LOGIN_URL, payload
        )
        self.assertEqual(response.status_code, 401)

    def test_verified_user_login(self):
        self.user.is_verified = True
        self.user.save()
        payload = {
            "email": self.email,
            "password": self.password
        }
        response = self.client.post(
            LOGIN_URL, payload
        )
        self.assertEqual(response.status_code, 200)

    def test_verified_user_login_then_logout(self):
        self.user.is_verified = True
        self.user.save()

        payload = {
            "email": self.email,
            "password": self.password
        }

        self.client.post(
            LOGIN_URL, payload
        )
        user = get_user_model().objects.last()
        tokens = RefreshToken().for_user(user)

        payload = {"refresh": str(tokens)}

        response = self.client.post(
            LOGOUT_URL, payload,
            HTTP_AUTHORIZATION=f"Bearer {tokens.access_token}"
        )
        self.assertEqual(response.status_code, 204)

    def test_password_reset(self):
        self.user.is_verified = True
        self.user.save()

        payload = {
            "email": self.email
        }

        response = self.client.post(
            PASSWORD_RESET, payload
        )
        self.assertEqual(response.status_code, 200)

    def test_password_reset_confirm(self):
        self.user.is_verified = True
        self.user.save()

        payload = {
            "email": self.email
        }
        self.client.post(
            PASSWORD_RESET, payload
        )
        user = get_user_model().objects.get(email=self.email)
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)

        id = smart_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)

        check = PasswordResetTokenGenerator().check_token(user, token)
        self.assertTrue(check)

        response = self.client.get(
            reverse("password-reset-confirm",
                    kwargs={"uidb64": uidb64, "token": token})
        )
        self.assertEqual(response.status_code, 200)

    def test_password_reset_complete(self):
        self.user.is_verified = True
        self.user.save()

        payload = {
            "email": self.email
        }
        self.client.post(
            PASSWORD_RESET, payload
        )
        user = get_user_model().objects.get(email=self.email)
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)

        id = smart_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)

        check = PasswordResetTokenGenerator().check_token(user, token)
        self.assertTrue(check)

        res = self.client.get(
            reverse("password-reset-confirm",
                    kwargs={"uidb64": uidb64, "token": token})
        )
        self.assertTrue(res)

        payload = {
            "password": "newpassword321",
            "uidb64": uidb64,
            "token": token
        }

        response = self.client.patch(
            PASSWORD_RESET_COMPLETE, payload, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
