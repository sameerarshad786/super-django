from django.urls import reverse

from core.tests.main_setup import MainSetup


POST_URL = reverse("post-create")

REMARK_URL = reverse("remark-create")

COMMENT_URL = reverse("comment-create")


class PostTest(MainSetup):
    def test_user_create_post(self):
        payload = {
            "text": "post for testing api's"
        }
        response = self.client.post(
            POST_URL, payload,
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.access_token}"
        )
        self.assertEqual(response.status_code, 201)

    def test_user_update_post(self):
        response = self.client.patch(
            reverse("post-update", args=[self.post_id]),
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.access_token}"
        )
        self.assertEqual(response.status_code, 200)

    def test_user_delete_post(self):
        response = self.client.delete(
            reverse("post-destroy", args=[self.post_id]),
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.access_token}"
        )
        self.assertEqual(response.status_code, 204)

    def test_user_remarks(self):
        payload = {
            "on_post": self.post_id,
            "popularity": "like"
        }
        response = self.client.post(
            REMARK_URL, payload,
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.access_token}"
        )
        self.assertEqual(response.status_code, 201)

    def test_user_remarks_update(self):
        payload = {
            "on_post": self.post_id,
            "popularity": "like"
        }
        _res = self.client.post(
            REMARK_URL, payload,
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.access_token}"
        )
        payload["popularity"] = "heart"
        response = self.client.patch(
            reverse("remark-update", args=[_res.data.get("id")]), payload,
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.access_token}",
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_user_remarks_delete(self):
        payload = {
            "on_post": self.post_id,
            "popularity": "like"
        }
        _res = self.client.post(
            REMARK_URL, payload,
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.access_token}"
        )
        response = self.client.delete(
            reverse("remark-destroy", args=[_res.data.get("id")]),
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.access_token}"
        )
        self.assertEqual(response.status_code, 204)

    def test_user_comment_on_post(self):
        payload = {
            "on_post": self.post_id,
            "comment": "nice keep it up"
        }
        response = self.client.post(
            COMMENT_URL, payload,
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.access_token}"
        )
        self.assertEqual(response.status_code, 201)

    def test_user_update_his_comment(self):
        payload = {
            "on_post": self.post_id,
            "comment": "my updated comment"
        }
        response = self.client.patch(
            reverse("comment-update", args=[self.comment_id]), payload,
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.access_token}",
            content_type="application-json"
        )
        self.assertEqual(response.status_code, 200)

    def test_user_delete_his_comment(self):
        response = self.client.delete(
            reverse("comment-destroy", args=[self.comment_id]),
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.access_token}"
        )
        self.assertEqual(response.status_code, 204)
