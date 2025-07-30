from celery import shared_task
from .utils import send_telegram_notification
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


@shared_task
def notify_borrowings_deadlines():
    deadline = now().date() + timedelta(days=1)
    borrowings = Borrowing.objects.filter(
        expected_return_date=deadline, actual_return_date__isnull=True, is_active=True
    )
    for borrowing in borrowings:
        message = f"🔔 Reminder: Deadline for task '{task.title}' is {task.deadline.strftime('%Y‑%m‑%d %H:%M')}"
        send_telegram_notification(task.user.telegram_chat_id, message)
        task.notified = True
        task.save()
