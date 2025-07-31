from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Borrowing
from library_service_api.utils.telegram import send_telegram_message

@receiver(post_save, sender=Borrowing)
def notify_new_borrowing(sender, instance, created, **kwargs):
    if created:
        message = (
            f"📚 New Borrowing Created\n\n"
            f"👤 Customer: {instance.customer}\n"
            f"📖 Book: {instance.book.title}\n"
            f"📅 Borrow Date: {instance.borrow_date}\n"
            f"📅 Expected Return: {instance.expected_return_date}"
        )
        send_telegram_message(message)
