from django.test import TestCase
from django.contrib.auth import get_user_model
from payments.models import Payment
from library.models import Borrowing, Book
from datetime import date
from decimal import Decimal

User = get_user_model()

class TestPaymentModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@email.com", password="testpassword")
        self.book = Book.objects.create(
            title="test_book",
            author="test_author",
            cover="soft",
            inventory=1,
            daily_fee=5.00)
        self.borrowing = Borrowing.objects.create(
            customer=self.user,
            book=self.book,
            borrow_date=date(2025, 7, 1),
            expected_return_date=date(2025, 7, 10)
        )

    def test_create_payment(self):
        payment = Payment.objects.create(
            user=self.user,
            borrowing=self.borrowing,
            amount=Decimal("50.00"),
            status=Payment.PaymentsStatus.pending,
            type=Payment.PaymentsType.PAYMENT,
            session_id="testsession123"
        )
        self.assertEqual(payment.amount, Decimal("50.00"))
        self.assertEqual(payment.user, self.user)
        self.assertEqual(payment.borrowing, self.borrowing)
        self.assertEqual(payment.status, Payment.PaymentsStatus.pending)
        self.assertEqual(payment.type, Payment.PaymentsType.PAYMENT)
        self.assertEqual(payment.session_id, "testsession123")