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