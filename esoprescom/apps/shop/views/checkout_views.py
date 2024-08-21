import random
import string
from django.shortcuts import render,get_object_or_404,redirect
from apps.dashboard.models.Address import Address
from apps.shop.services.payment_service import StripeService
from apps.shop.services.cart_service import CartService
from apps.shop.models.Carrier import Carrier
from apps.shop.models.Order import Order
from apps.shop.models.Orderdetails import Orderdetails
from apps.shop.models.Method import Method
from apps.accounts.models.Customer import Customer
from apps.shop.forms.checkoutAddressForm import checkoutAddressForm
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.db import transaction


def index(request):
    carrier_id = request.GET.get('carrier_id')
    addresse_billing_id = request.GET.get('addresse_billing_id','')
    addresse_shipping_id = request.GET.get('addresse_shipping_id',addresse_billing_id)
    new_shipping_address = request.GET.get('new_shipping_address','')
    if addresse_billing_id and addresse_billing_id !='':
       addresse_billing_id = int(addresse_billing_id)
    if addresse_shipping_id and addresse_shipping_id !='':
       addresse_shipping_id = int(addresse_shipping_id)

    ready_to_pay = False
    if new_shipping_address and new_shipping_address != 'false':
       ready_to_pay = bool(addresse_billing_id) and bool(addresse_shipping_id)
    else:
       ready_to_pay = bool(addresse_billing_id)
      
    if carrier_id and carrier_id!='':
      carrier = Carrier.objects.filter(id=carrier_id).first()
      if carrier:
        request.session['carrier'] =  {
              'id':carrier.id,  
              'name':carrier.name,  
              'price':carrier.price  
        }
    cart = CartService.get_cart_details(request)
    order_id = None
    if ready_to_pay:
      #create order
      if new_shipping_address and new_shipping_address != 'false':
         billing_address = Address.objects.filter(id=addresse_billing_id).first()
         shipping_address = Address.objects.filter(id=addresse_shipping_id).first()
      else:
         billing_address = Address.objects.filter(id=addresse_billing_id).first()
         shipping_address=None  
      billing_address_str = billing_address.get_address_as_string() if billing_address else ""
      shipping_address_str = shipping_address.get_address_as_string() if shipping_address else ""
      order_id = create_order(request,billing_address_str,shipping_address_str)

    payment_service = StripeService() 
    #print("payment_service.get_public_key:",payment_service.get_public_key)
    carriers = Carrier.objects.all()
    address_form = checkoutAddressForm()
    #print("addresse_billing_id:",addresse_billing_id)
    return render(request,"shop/checkout.html",{
     'cart':cart,
     'carriers':carriers,
     'address_form':address_form,
     'ready_to_pay':ready_to_pay,
     'addresse_billing_id':addresse_billing_id,
     'addresse_shipping_id':addresse_shipping_id,
     'new_shipping_address':new_shipping_address,
     'order_id':order_id,
     'public_key':payment_service.get_public_key,
     })

def add_address(request):
    user = request.user
    if request.method == 'POST':
      if not user.is_authenticated:
        email = request.POST.get('email')
        existing_user = Customer.objects.filter(email=email).first()
        if existing_user:
          login(request,existing_user)
        else:
          new_user= Customer()  
          new_user.username = email
          new_user.email = email
          password = ''.join(random.choices(string.ascii_letters+string.digits,k=8))
          new_user.password = make_password(password)
          #envoie de mail de creation de compte avec mot de passe
          new_user.save()
          login(request,new_user)
          user = new_user
      address_form = checkoutAddressForm(request.POST)
      if address_form.is_valid():
         address = address_form.save(commit=False)
         address.author = user 
         address.save()
         messages.success(request,'Address added succesfully')

    return redirect('shop:checkout')

def login_form(request):
   if request.user.is_authenticated:
      messages.success(request,'You are already logged in')
      return JsonResponse({'isSucces':True,
                           'message':'This user is already connected'})
   if request.method == "POST":
      email= request.POST.get('email')
      password= request.POST.get('password')
      
      user = authenticate(request,username=email,password=password)
      if user is not None:
        login(request,user)
        return JsonResponse({'isSuccess':True,
                          'message':'This user connected'})
      else:  
        return JsonResponse({'isSuccess':False,
                          'message':'Invalid credentiel'})
   return JsonResponse({'isSuccess':False,
                          'message':'Error request method',
                          #'email':email,
                          #'password':password
                          })


def create_order(request,billing_address,shipping_address=None):
    user = request.user
    cart = CartService.get_cart_details(request)
    carrier = request.session.get('carrier',Carrier.objects.first())
    
    order = Order()
    order.client_name = user.username
    order.billing_address =   billing_address                 
    order.shipping_address =  shipping_address or billing_address                  
    order.carrier_name =   carrier.name                 
    order.carrier_price =   carrier.price                 
    order.quantity =  cart['cart_count']                  
    order.order_cost =   cart['sub_total_ht']                 
    order.taxe =       cart['taxe_amount']              
    order.order_cost_ttc =  cart['sub_total_with_shipping']  
    order.payment_method ='Stripe'
    order.author = user
    order.save()

    #order detail
    with transaction.atomic():
      for item in cart['items']:
        order_details = Orderdetails()
        """
        order_details.product_name = item['product']['name']
        order_details.product_description = item['product']['description']
        order_details.solde_price = item['product']['solde_price']
        order_details.regular_price = item['product']['regular_price']
        order_details.quantity = item['quantity']
        order_details.taxe = item['taxe_amount']
        order_details.sub_total_ht = item['sub_total_ht']
        order_details.sub_total_ttc = item['sub_total_ttc']
        order_details.order = order
        order_details.save
        """
        order_details.product_name = item.get('product').get('name')
        order_details.product_description = item.get('product').get('description')
        order_details.solde_price = item.get('product').get('solde_price')
        order_details.regular_price = item.get('product').get('regular_price')
        order_details.quantity = item.get('quantity')
        order_details.taxe = item.get('taxe_amount')
        order_details.sub_total_ht = item.get('sub_total_ht')
        order_details.sub_total_ttc = item.get('sub_total_ttc')
        order_details.order = order
        order_details.save()
    return order.id


                