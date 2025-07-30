import requests
from django.conf import settings


def send_telegram_notification(chat_id, message):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }
    response = requests.post(url, json=payload)
    return response.json()
