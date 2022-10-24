from django.urls import reverse

from core.tests.main_setup import MainSetup


LOGIN_URL = reverse("login")


class UserProfileTest(MainSetup):
    def test_retrieve_profile(self):
        self.assertTrue(self.profile)

        response = self.client.get(
            reverse("profile-retrieve", args=[self.profile.id]),
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.access_token}"
        )
        self.assertEqual(response.status_code, 200)

    def test_update_verified_user_profile(self):
        self.assertTrue(self.profile)

        response = self.client.patch(
            reverse("profile-update", args=[self.profile.id]),
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.access_token}"
        )
        self.assertEqual(response.status_code, 200)

    def test_update_someone_profile_failed(self):
        self.assertTrue(self.profile)

        response = self.client.patch(
            reverse("profile-update",
                    args=["0db2ad5c-cca2-47e1-a1b1-3ba0d006023a"]),
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.access_token}"
        )
        self.assertEqual(response.status_code, 404)
