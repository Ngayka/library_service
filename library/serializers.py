from rest_framework import serializers

from library.models import Book


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title"]

class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title", "author", "cover", "inventory", "daily_fee"]

class BorrowingSerializer(serializers.ModelSerializer):
    borrow_date = serializers.DateField(format="%d/%m/%Y", input_formats=["%d/%m/%Y"])
    expected_return_date = serializers.DateField(format="%d/%m/%Y", input_formats=["%d/%m/%Y"])
    actual_return_date = serializers.DateField(format="%d/%m/%Y", input_formats=["%d/%m/%Y"], required=False)