from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework_simplejwt.tokens import RefreshToken

from ..models import User


class Util:
    @staticmethod
    def send_activation_mail(data):
        user = User.objects.get(email=data["user_data"]["email"])
        current_site = get_current_site(data["request"]).domain
        relativeLink = reverse("verify-email")
        token = RefreshToken().for_user(user)
        absurl = f"{current_site}{relativeLink}?token={str(token)}"
        html_content = render_to_string(
            "auth_mails/registration_mail.html",
            {"absurl": absurl}
        )
        msg = EmailMessage(
            subject="Registration Mail", body=html_content,
            to=[user]
        )
        msg.content_subtype = "html"
        msg.send()

    def password_reset_mail(data):
        user = User.objects.get(email=data["request"].data["email"])
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        current_site = get_current_site(request=data["request"]).domain
        relativeLink = reverse(
            "password-reset-confirm",
            kwargs={"uidb64": uidb64, "token": token}
        )
        absurl = f"http://{current_site}{relativeLink}?token={token}"
        html_content = render_to_string(
            "auth_mails/password_reset_mail.html",
            {"absurl": absurl}
        )
        msg = EmailMessage(
            subject="Password Reset", body=html_content,
            to=[user]
        )
        msg.content_subtype = "html"
        msg.send()
