from datetime import date

from django.test import TestCase
from django.contrib.auth import get_user_model
from library.models import Borrowing, Book

User = get_user_model()

class BookTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title="Book Title",
                                        author="Author",
                                        cover="soft",
                                        daily_fee=5.00,
                                        inventory=2
                                        )
    def test_book_info(self):
        self.assertEqual(self.book.title, "Book Title")
        self.assertEqual(self.book.author, "Author")
        self.assertEqual(self.book.cover, "soft")
        self.assertEqual(self.book.daily_fee, 5.00)
        self.assertEqual(self.book.inventory, 2)

        self.book.inventory -= 1
        self.book.save()
        self.assertEqual(self.book.inventory, 1)

class BorrowingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@email.com", password="test_password")
        self.book = Book.objects.create(title="Book Title",
                                        author="Author",
                                        cover="soft",
                                        daily_fee=5.00,
                                        inventory=2
                                        )

    def test_create_borrowing(self):
        borrowing = Borrowing.objects.create(
            customer=self.user,
            book=self.book,
            borrow_date=date(2025, 7, 1),
            expected_return_date=date(2025, 7, 10,),
            notified=False
        )

        self.assertEqual(borrowing.customer, self.user)
        self.assertEqual(borrowing.book, self.book)
        self.assertEqual(borrowing.borrow_date, date(2025, 7, 1))
        self.assertEqual(borrowing.expected_return_date, date(2025, 7, 10))
        self.assertIsNone(borrowing.actual_return_date)
