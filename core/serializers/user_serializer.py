from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework import serializers
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from core.models.user_model import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=255, min_length=6
    )
    confirm_password = serializers.CharField(
        max_length=255, min_length=6, write_only=True
    )

    class Meta:
        model = User
        fields = ("email", "password", "confirm_password")

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = User.objects.filter(email=email)

        if user.exists():
            raise serializers.ValidationError(
                _("This email is already registered"))

        if password != attrs.get("confirm_password"):
            raise serializers.ValidationError(
                _("both passwords does not match"))

        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField()

    class Meta:
        model = User
        fields = ("token")


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=30, read_only=True
    )
    email = serializers.EmailField(
        max_length=50, write_only=True
    )
    password = serializers.CharField(
        max_length=255, min_length=6, write_only=True
    )
    tokens = serializers.JSONField(
        read_only=True
    )

    class Meta:
        model = User
        fields = ("username", "email", "password", "tokens")

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)

        if user:
            if user.is_deactivate_by_admin:
                raise exceptions.AuthenticationFailed(_(
                    "you are ban from pak social"
                ))

            elif not user.is_active:
                raise exceptions.AuthenticationFailed(_(
                    "user is disabled"
                ))

            elif not user.is_verified:
                raise exceptions.AuthenticationFailed(_(
                    "user is not verified"
                ))

        if not user:
            raise exceptions.AuthenticationFailed(_(
                "user does not exists"
            ))

        return {
            "email": user.email,
            "tokens": user.tokens
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    class Meta:
        model = User
        fields = ("refresh")

    default_error_messages = {
        "bad_token": _("Token is expired or invalid")
    }

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            return RefreshToken(self.token).blacklist()
        except TokenError:
            return self.fail("bad_token")


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=50
    )

    class Meta:
        model = User
        fields = ("email")

    def validate(self, attrs):
        email = attrs.get("email")

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(_(
                "This email does not exists"
            ))

        return attrs


class ResetPasswordCompleteSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, min_length=6
    )
    uidb64 = serializers.CharField()
    token = serializers.CharField()

    class Meta:
        fields = ("password", "uidb64", "token")

    def validate(self, attrs):
        password = attrs.get("password")
        uidb64 = attrs.get("uidb64")
        token = attrs.get("token")

        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)

        if PasswordResetTokenGenerator().check_token(user, token):
            user.set_password(password)
            user.save()
            return user

        raise exceptions.AuthenticationFailed(_(
            "user is not found"
        ))
