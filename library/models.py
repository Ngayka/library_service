from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model

from django.core.validators import MinValueValidator
from django.db import models

from customer.models import User

class Book(models.Model):
    class StatusChoices(models.TextChoices):
        soft = "Soft"
        hard = "Hard"

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    cover = models.CharField(max_length=100, choices = StatusChoices.choices)
    inventory = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        help_text="Number of available books"
    )
    daily_fee = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    def __str__(self):
        return f"{self.title} by {self.author}"

class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(
        null=True,
        blank=True
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowings')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Payment(models.Model):
    class PaymentsStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"

    class PaymentsType(models.TextChoices):
        PAYMENT = "PAYMENT", "Payment"
        FINE = "FINE", "Fine"
    status = models.CharField(max_length=100, choices=PaymentsStatus.choices)
    type = models.CharField(max_length=100, choices=PaymentsType.choices)
    borrowing = models.ForeignKey(Borrowing,
                                  on_delete=models.CASCADE,
                                  related_name='payments')
    session_url = models.URLField()
    session_id = models.CharField(max_length=100)
    money_to_pay = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    def __str__(self):
        return f"{self.type} - {self.status} - ${self.money_to_pay}"
