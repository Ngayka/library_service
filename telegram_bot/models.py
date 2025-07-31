from django.db import models
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
        response = self.client.post(
            "/telegram/webhook/",
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.telegram_chat_id, 12345)

    def test_webhook_wrong_token(self):
        data = {
            "message": {
                "chat": {"id": 12345},
                "text": "/start wrongtoken"
            }
        }
        response = self.client.post(
            "/telegram/webhook/",
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertIsNone(self.user.telegram_chat_id)

    def test_webhook_post_without_message(self):
        response = self.client.post(
            "/telegram/webhook/",
            data=json.dumps({}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"ok": True})

    def test_webhook_get_method_not_allowed(self):
        response = self.client.get("/telegram/webhook/")
        self.assertEqual(response.status_code, 405)
