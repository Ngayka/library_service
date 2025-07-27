from django.shortcuts import render
from rest_framework import viewsets, permissions

from library.models import Book
from library.serializers import BookListSerializer, BookDetailSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        return BookDetailSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy", "create"]:
            return [permissions.IsAdminUser()]
        elif self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
