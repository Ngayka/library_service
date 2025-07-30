from django.urls import path, include
from rest_framework import routers

from library.views import BookViewSet, BorrowingViewSet

app_name = "library"


router = routers.DefaultRouter()
router.register("books", BookViewSet, basename="books")
router.register("borrowings", BorrowingViewSet, basename="borrowings")

urlpatterns = [path("", include(router.urls))]
