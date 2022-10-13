from django.test import TestCase
from django.urls import reverse

from core.models.user_model import User
from profiles.models.profile_model import Profile


class UserProfileTest(TestCase):
    def setUp(self) -> None:
        self.email = "testuser@paksocial.com"
        self.password = "testing321"

    def test_verified_user_profile_create(self):
        user = User.objects.create_user(
            email=self.email, password=self.password
        )
        user.is_verified = True
        if user.is_verified:
            profile = Profile.objects.create(user=user)
            self.assertTrue(profile)
        self.assertTrue("user is not verified")

    def test_unverified_user_profile_create(self):
        user = User.objects.create_user(
            email=self.email, password=self.password
        )
        if user.is_verified:
            profile = Profile.objects.create(user=user)
            self.assertTrue(profile)
        self.assertTrue("user is not verified")
