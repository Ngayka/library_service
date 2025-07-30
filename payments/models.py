from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
from library.models import Borrowing


class Payment(models.Model):
    class PaymentsStatus(models.TextChoices):
        pending="Pending"
        succeeded="Succeeded"
        canceled="Canceled"

    class PaymentsType(models.TextChoices):
        PAYMENT = "PAYMENT", "Payment"
        FINE = "FINE", "Fine"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=120, unique=True)
    status = models.CharField(max_length=100, choices=PaymentsStatus.choices)
    type = models.CharField(max_length=100, choices=PaymentsType.choices, default="Pending")
    payments_intent = models.CharField(max_length=120, blank=True, null=True)
    amount = models.DecimalField(max_digits=5,
                                decimal_places=2,
                                validators=[MinValueValidator(Decimal('0.00'))]
                                 )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Payment {self.id} - {self.status}: {self.amount}"

