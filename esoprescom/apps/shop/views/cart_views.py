from django.shortcuts import render,redirect,get_object_or_404
from apps.shop.models.Carrier import Carrier
from apps.shop.models.Product import Product
from apps.shop.services.cart_service import CartService


def index(request):
  """
  cart = request.session.get('cart',{})
  data = []
  for id,quantity in cart.items():
    product = get_object_or_404(Product,id=id)
    data.append({'product':product,'quantity':quantity})
  """
  carrier_id = request.GET.get('carrier_id')
  if carrier_id and carrier_id!='':
      carrier = Carrier.objects.filter(id=carrier_id).first()
      if carrier:
        request.session['carrier'] =  {
              'id':carrier.id,  
              'name':carrier.name,  
              'price':carrier.price  
        }
  cart = CartService.get_cart_details(request)
  if not len(cart['items']):
    return redirect('shop:shop_list')
      
  carriers = Carrier.objects.all()
  
  return render(request,'shop/cart.html',{'cart':cart,'carriers':carriers})

def add_to_cart(request,product_id):
  CartService.add_to_cart(request,product_id,1)

  return redirect('shop:cart')

def remove_from_cart(request,product_id,quantity=1):
  CartService.remove_from_cart(request,product_id,quantity)

  return redirect('shop:cart')

def clear_cart(request):
  CartService.clear_cart(request)

  return redirect('shop:cart')
