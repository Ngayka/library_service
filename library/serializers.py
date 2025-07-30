from django.db import transaction
from rest_framework import serializers

from library.models import Book, Borrowing


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title"]

class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title", "author", "cover", "inventory", "daily_fee"]

class BorrowingSerializer(serializers.ModelSerializer):
    borrow_date = serializers.DateField(format="%d.%m.%Y", input_formats=["%d.%m.%Y", "%Y-%m-%d"])
    expected_return_date = serializers.DateField(format="%d.%m.%Y", input_formats=["%d.%m.%Y", "%Y-%m-%d"])
    actual_return_date = serializers.DateField(format="%d.%m.%Y", input_formats=["%d.%m.%Y", "%Y-%m-%d"], required=False)
    is_active = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Borrowing
        fields = ["id", "book", "borrow_date", "expected_return_date", "actual_return_date", "is_active"]

    def create(self, validated_data):
        user = self.context["request"].user
        book = validated_data["book"]

        with transaction.atomic():
            book_locked = Book.objects.select_for_update().get(pk=book.id)
            if book_locked.inventory < 1:
                raise serializers.ValidationError(f"There is no {book.title} book available.")
            book_locked.inventory -= 1
            book_locked.save()
            borrowing = Borrowing.objects.create(customer=user, **validated_data)
        return borrowing

    def update(self, instance, validated_data):
        if not instance.actual_return_date and validated_data.get("actual_return_date"):
            instance.book.inventory += 1
            instance.book.save()
        return super().update(instance, validated_data)

    def get_is_active(self, obj):
        return obj.actual_return_date is None


