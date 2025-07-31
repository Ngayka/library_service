from celery import shared_task
from .utils import send_telegram_notification

from datetime import datetime, timedelta
from django.utils.timezone import now
from library.models import Borrowing


@shared_task
def notify_borrowings_deadlines():
    deadline = now().date() + timedelta(days=1)
    borrowings = Borrowing.objects.filter(
        expected_return_date=deadline, actual_return_date__isnull=True, is_active=True, notified=False
    )
    for borrowing in borrowings:
        message = f"🔔 Reminder: Deadline for book '{borrowing.book.title}' is {borrowing.expected_return_date.strftime('%Y‑%m‑%d')}"
        send_telegram_notification(borrowing.user.telegram_chat_id, message)
        borrowing.notified = True
        borrowing.save()
