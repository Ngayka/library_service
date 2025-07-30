from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY

def payment_form(request):
    return render(request, 'payment_form.html')

@csrf_exempt
def create_checkout_session(request, borrowing_id) -> None:
    borrowing = get_object_or_404(Borrowing, pk=borrowing_id)
    days = (borrowing.expected_return_date - borrowing.borrowing_date).days
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
            return redirect(checkout_session.url)
        except Exception as e:
            return JsonResponse({'error': str(e)})


def create_late_fee_payment(request, borrowing_id):
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
            return redirect(checkout_session.url)
        except Exception as e:
            return JsonResponse({'error': str(e)})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def payment_success(request):
    return render(request, 'payment_success.html')

def payment_cancel(request):
    return render(request, 'payment_canceled.html')

