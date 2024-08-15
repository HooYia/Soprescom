from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from shop.models.Order  import Order


@login_required
def index(request):
  user = request.user
  if not user.is_authenticated:
    return redirect('shop:home')
  orders =  Order.objects.prefetch_related('order_details').filter(author=user,is_paid=True)
  
  return render(request,"dashboard/index.html",{
    'page':'orders',
    'orders':orders,    
    })