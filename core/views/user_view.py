import jwt

from django.conf import settings
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from core.serializers.user_serializer import (
    RegisterSerializer, EmailVerificationSerializer,
    LoginSerializer, LogoutSerializer, ResetPasswordSerializer,
    ResetPasswordCompleteSerializer
)
from core.models.user_model import User
from core.utils.auth_mails import Util

from rest_framework import generics, views, permissions, status
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        data = {
            "user_data": user_data,
            "request": request,
        }
        Util.send_activation_mail(data)
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

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class ResetPasswordAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        data = {
            "request": request
        }
        Util.password_reset_mail(data)
        return Response(
            {"message": "Email has been sent"},
            status=status.HTTP_200_OK
        )


class ResetPasswordConfirmAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self, request, uidb64, token):
        id = smart_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response(
                {"message": "token is invalid"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"message": "token is valid"},
            status=status.HTTP_200_OK
        )


class ResetPasswordCompleteAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordCompleteSerializer
    permission_classes = (permissions.AllowAny,)

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"message": "Password Reset successful"},
            status=status.HTTP_200_OK
        )
