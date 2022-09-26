import jwt

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings

from core.serializers.user_serializer import (
    RegisterSerializer, EmailVerificationSerializer,
    LoginSerializer, LogoutSerializer
)
from core.models.user_model import User
from core.utils.auth_mails import Util

from rest_framework import generics, views, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data["email"])

        token = RefreshToken().for_user(user)
        current_site = get_current_site(request).domain
        relativeLink = reverse("verify-email")

        absurl = f"http://{current_site}{relativeLink}?token={str(token)}"

        data = {
            "email_subject": "Registration Link",
            "absurl": absurl,
            "to_email": user.email,
        }

        Util.send_registration_mail(data)

        return Response(
            {"message": "we have sent you an email with instruction"},
            status=status.HTTP_201_CREATED
        )


class EmailVerificationAPIView(views.APIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = (permissions.AllowAny,)

    token_param_config = openapi.Parameter(
        "token", in_=openapi.IN_QUERY,
        description="email verication token", type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get("token")
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])

            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response(
                {"message": "Email Successfully Activated"},
                status=status.HTTP_200_OK
            )

        except jwt.ExpiredSignatureError:
            return Response(
                {"message": "Registration Link has been expired"},
                status=status.HTTP_400_BAD_REQUEST
            )

        except jwt.exceptions.DecodeError:
            return Response(
                {"message": "Invalid Link"},
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"user": f"{request.data.get('email')}", "data": serializer.data},
            status=status.HTTP_200_OK
        )


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
