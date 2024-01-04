import json

import stripe
from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from cart.cart import Cart
from orders.views import payment_confirmation

# Displays the order confirmation page.
def order_placed(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'payment/orderplaced.html')

# Displays the order error page.
def error(request):
    return render(request, 'payment/error.html')

@login_required
def CartView(request):
    cart = Cart(request)
    total = str(round(cart.get_total(), 2))
    total = int(float(total) * 100)

    stripe.api_key = 'sk_test_51KHfkzEeX9bmWjgu3gYM9xx50dvPIbkrUJq697PEhJQgR4q2zM3IM5feYxzeGKHDtUoQA733S5vJSosjMO7kwTeR00LKx47TQe'
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='usd',
        metadata={'userid': request.user.id}
    )

    return render(request, 'payment/checkout.html', {'client_secret': intent.client_secret})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)