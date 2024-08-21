
from django.shortcuts import render,get_object_or_404,redirect
from apps.shop.models.Order  import Order
import stripe
from django.http import JsonResponse
from apps.shop.services.payment_service import StripeService


def index(request,order_id):
  payment_service = StripeService() 
  stripe.api_key = payment_service.get_private_key()
  #print('stripe.api_key:',stripe.api_key)
  #if order_id: 
  #  order_id = int(order_id)
  try:  
        
        order  = get_object_or_404(Order,id=order_id)
        # stripe divise tous montant par 100. 
        # Donc on multiplie tous les montants par 100
        amount = int(order.order_cost_ttc * 100)
        # Create a PaymentIntent with the order amount and currency
        payment_indent = stripe.PaymentIntent.create(
            amount   = amount,
            currency = 'eur',
            # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
            automatic_payment_methods={
                'enabled': True,
            },
        )
        order.strip_payment_intent = payment_indent['id']
        order.save()
        return JsonResponse({
            'clientSecret': payment_indent['client_secret']
        })
  except Exception as e:
        return JsonResponse({"error": str(e)})


def payment_success(request):
    payment_intent_id = request.GET.get('payment_intent')
    if not payment_intent_id:
        print('Le parametre payment_intent est manquant dans la requete')
        return redirect('shop:home')
    #print(order)
    try:
        #control que les ID correxponde entre strip et notre base
        payment_service = StripeService() 
        stripe.api_key = payment_service.get_private_key()
        payment = stripe.PaymentIntent.retrieve(payment_intent_id)
        if payment.status == 'succeeded' :
          order = get_object_or_404(Order,strip_payment_intent=payment_intent_id)
          order.is_paid = True
          order.save()
          print('Paiement reussi')
          return render(request,'shop/payment_succes.html',{})
        else:
          print(f"Etat du paaiement non reussi: {payment.status}")
          return redirect('shop:home')
    except stripe.error.StripeError as e:
         print(f"Erreur stripe: {str(e)}")
         return redirect('shop:home')
    except Exception as e:
          print(f"Une Erreur s'est produite: {str(e)}")
          return redirect('shop:home')
        
    #return render(request,'shop/payment_succes.html',{})
  
  