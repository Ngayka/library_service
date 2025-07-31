import json
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class TelegramWebhookTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="password123",
            telegram_token="abc123"
        )

    def test_webhook_start_valid_token(self):
        data = {
            "message": {
                "chat": {"id": 12345},
                "text": "/start abc123"
            }
        }
        url = reverse("telegram_webhook")
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(int(self.user.telegram_chat_id), 12345)

    def test_webhook_wrong_token(self):
        data = {
            "message": {
                "chat": {"id": 12345},
                "text": "/start wrongtoken"
            }
        }
        url = reverse("telegram_webhook")
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertIsNone(self.user.telegram_chat_id)

    def test_webhook_post_without_message(self):
        url = reverse("telegram_webhook")
        response = self.client.post(
            url,
            data=json.dumps({}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"ok": True})

    def test_webhook_get_method_not_allowed(self):
        url = reverse("telegram_webhook")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)
