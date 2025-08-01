from decimal import Decimal
from django.core.validators import MinValueValidator
from django.conf import settings
from django.contrib.auth import get_user_model


from django.db import models

from customer.models import User


class Book(models.Model):
    class StatusChoices(models.TextChoices):
        soft = "Soft"
        hard = "Hard"

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    cover = models.CharField(max_length=100, choices=StatusChoices.choices)
    inventory = models.PositiveIntegerField(
        validators=[MinValueValidator(0)], help_text="Number of available books"
    )
    daily_fee = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )

    def __str__(self):
        return f"{self.title} by {self.author}"


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notified = models.BooleanField(default=False)
