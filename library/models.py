from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

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