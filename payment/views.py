import stripe
import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from order.views import payment_confirmation
from basket.basket import Basket

# Create your views here.

@login_required
def BasketView(request):
    basket = Basket(request)
    # total = int(float(str(basket.get_total_price()).replace(',','')))
    stripe.api_key = 'sk_test_51OFOdQDTLjUNiCyryEZw0y5gEpeuc0N7okJ4htW79o1DpXb7DbyIOhwO5lCADnHadjGIrtKMuNdWyaxW4cHcaUMa00w2DdwGON'
    intent = stripe.PaymentIntent.create(
        amount= 200, 
        currency = 'gbp',      
        metadata={'userid':request.user.id}
    )
    return render(request, 'payment/home.html', {'client_secret':intent.client_secret})


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
        print('Unhanded event type {}'.format(event.type))
    return HttpResponse(status=200)


def order_placed(request):
        basket = Basket(request)
        basket.clear()
        return render(request, 'payment/orderplaced.html')