from django.utils import timezone
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from telegram_bot.utils import send_telegram_message
from library.models import Book, Borrowing
from library.serializers import (
    BookListSerializer,
    BookDetailSerializer,
    BorrowingSerializer,
)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        return BookDetailSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy", "create"]:
            return [permissions.IsAdminUser()]
        elif self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        book = serializer.save()
        send_telegram_message(f"Add new book {book.title}, author: {book.author}")

class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related("customer", "book").all()
    serializer_class = BorrowingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Borrowing.objects.all()
        is_active = self.request.query_params.get("is_active")
        user_id = self.request.query_params.get("customer_id")

        if user_id:
            queryset = queryset.filter(customer_id=user_id)

        if is_active == "True":
            queryset = queryset.filter(actual_return_date__isnull=True)
        elif is_active == "False":
            queryset = queryset.filter(actual_return_date__isnull=False)

        return queryset

    def perform_create(self, serializer):
        borrowing = serializer.save()
        send_telegram_message(f"Add new borrowing at {borrowing.borrowing_date} for book {borrowing.book.title}")


    @action(detail=True, methods=["post"], url_path="return")
    def return_book(self, request, pk=None):
        borrowing = self.get_object()
        if borrowing.actual_return_date is not None:
            return Response({"detail": "Book is already returned"}, status=400)
        serializer = self.get_serializer(
            borrowing, data={"actual_return_date": timezone.now().date()}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
