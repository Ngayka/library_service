from customer.views import CreateUserView, ManageUserView
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


app_name = "customer"
urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create_user"),
    path("me/", ManageUserView.as_view(), name="manage_user"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
