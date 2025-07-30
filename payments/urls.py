from django.urls import path
from rest_framework.routers import DefaultRouter
from payments.views import (
    PaymentViewSet,
    payment_form,
    CreateCheckoutSessionView,
    CreateLateFeePaymentView,
    payment_success,
    payment_cancel,
    stripe_webhook,
)

app_name = "payments"

router = DefaultRouter()
router.register("payments", PaymentViewSet, basename="payments")
urlpatterns = [
    path("pay/", payment_form, name="payment_form"),
    path(
        "create-checkout-session/<int:borrowing_id>/",
        CreateCheckoutSessionView.as_view(),
        name="create_checkout_session",
    ),
    path(
        "create-late-fee-payment/<int:borrowing_id>/",
        CreateLateFeePaymentView.as_view(),
        name="create_late_fee_payment",
    ),
    path("success/", payment_success, name="payment_success"),
    path("cancel/", payment_cancel, name="payment_cancel"),
    path("webhook/", stripe_webhook, name="stripe-webhook"),
]

urlpatterns += router.urls
