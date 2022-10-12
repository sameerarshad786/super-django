from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
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
    tokens = serializers.CharField(
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
                raise AuthenticationFailed(_(
                    "you are ban from pak social"
                ))

            elif not user.is_active:
                raise AuthenticationFailed(_(
                    "user is disabled"
                ))

            elif not user.is_verified:
                raise AuthenticationFailed(_("user is not verified"))

        if not user:
            raise AuthenticationFailed(_("user does not exists"))

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
