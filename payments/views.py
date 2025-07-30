from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from decimal import Decimal
from payments.serializers import PaymentSerializer
from payments.models import Payment
from library.models import Borrowing
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponseNotAllowed
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY

def payment_form(request):
    return render(request, 'payment_form.html')

class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, borrowing_id):
        borrowing = get_object_or_404(Borrowing, pk=borrowing_id)
        days = (borrowing.expected_return_date - borrowing.borrow_date).days
        amount = int(days * (borrowing.book.daily_fee * 100))
        if request.method == 'POST':
            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[
                        {
                            'price_data': {
                                'currency': 'usd',
                                'unit_amount': amount,
                                'product_data': {
                                    'name': f'Payment for borrowing #{borrowing_id}',
                                },
                            },
                            'quantity': 1,
                        },
                    ],
                    mode='payment',
                    success_url=request.build_absolute_uri('/payment_success/'),
                    cancel_url=request.build_absolute_uri('/payment_canceled/'),
                )
                payment = Payment.objects.create(user=request.user,
                                                 amount=Decimal(str(amount / 100)),
                                                 session_id=checkout_session.id,
                                                 status=Payment.PaymentsStatus.pending,
                                                 type=Payment.PaymentsType.PAYMENT)
                payment.save()
                return redirect(checkout_session.url)
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            return HttpResponseNotAllowed(['POST'])


class CreateLateFeePaymentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, borrowing_id):
        borrowing = get_object_or_404(Borrowing, pk=borrowing_id)

        if not borrowing.actual_return_date:
            return JsonResponse({'error': 'Book not yet returned'}, status=400)

        late_days = (borrowing.actual_return_date - borrowing.expected_return_date).days

        if late_days <= 0:
            return JsonResponse({'message': 'No late fee required'}, status=200)

        amount = int(late_days * borrowing.book.daily_fee * 100)

        if request.method == 'POST':
            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[
                        {
                            'price_data': {
                                'currency': 'usd',
                                'unit_amount': amount,
                                'product_data': {
                                    'name': f'Late fee for borrowing #{borrowing_id}',
                                },
                            },
                            'quantity': 1,
                        },
                    ],
                    mode='payment',
                    success_url=request.build_absolute_uri('/payments/late_success/'),
                    cancel_url=request.build_absolute_uri('/payments/late_cancel/'),
                )
                payment = Payment.objects.create(user=request.user,
                                                 amount=Decimal(str(amount / 100)),
                                                 session_id=checkout_session.id,
                                                 status=Payment.PaymentsStatus.pending,
                                                 type=Payment.PaymentsType.FINE)
                payment.save()
                return redirect(checkout_session.url)

            except Exception as e:
                return JsonResponse({'error': str(e)})

        return JsonResponse({'error': 'Invalid request method'}, status=400)

def payment_success(request):
    return render(request, 'payment_success.html')

def payment_cancel(request):
    return render(request, 'payment_canceled.html')


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print("💰 Payment was successful!")

    return HttpResponse(status=200)


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Payment.objects.filter(user=user).order_by('-created_at')
        borrowing_id = self.resuest.query_params.get('borrowing')
        if borrowing_id:
            queryset = queryset.filter(borrowing_id=borrowing_id)
        return queryset