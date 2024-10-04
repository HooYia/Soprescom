import logging

from apps.shop.models.Product import ActionLog, Stock, Product, Category
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from django.contrib import messages
from django.db import transaction
from apps.shop.models.Image import Image
from django.utils.translation import gettext as _


from django.utils.text import slugify
from load_task_in_production import search_serpapi_images, save_images_for_product


logger = logging.getLogger(__name__)

@login_required
def stock(request):
    
    #write your code logic here
    stocks = Stock.objects.all().select_related('stock_produit')
    products = Product.objects.exclude(produit_stock__isnull=False)

    
    context = {
        'stocks': stocks,
        'products': products,
        'calculate_difference': lambda stock: stock.initial_quantite - stock.quantite,
        'page':'stock',
        'subpage':'stock_tab',
    }
    return render(request, 'servicedsi/index.html', context)


@login_required
def add_stock(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantite = int(request.POST.get('quantite'))
        stockLimite = int(request.POST.get('stockLimite'))
    
        
        product = get_object_or_404(Product, id=product_id)
        stock, created = Stock.objects.get_or_create(
            stock_produit=product,
            defaults={'quantite': quantite, 'initial_quantite': quantite, 'stockLimite': stockLimite}
        )
        
        if not created:
            return JsonResponse({'error': 'Stock for this product already exists.'}, status=400)
        
        # Create an action log for adding stock
        ActionLog.objects.create(
            product_name=product.name,
            action_done_by=request.user.username,
            date_created=timezone.now()  # Store the current timestamp as date_created
        )
        return redirect('serviceapresvente:stock')
    
    products = Product.objects.exclude(stock__isnull=False)
    
    context = {
        'products': products,
        'page':'stock',
        'subpage':'stock_tab',
    }
    return render(request, 'servicedsi/index.html', context)

@login_required
def update_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    if request.method == 'POST':
        new_quantite = int(request.POST.get('added_quantite'))
        stockLimite = int(request.POST.get('stockLimite'))
        
        difference = new_quantite
        actual_quantity = new_quantite + stock.quantite
        stock.initial_quantite += difference
        stock.quantite = actual_quantity
        stock.stockLimite = stockLimite
        stock.save()
        
        # Create an action log for updating stock
        ActionLog.objects.create(
            product_name=stock.stock_produit.name,
            action_done_by=request.user.username,
            date_modified=timezone.now()  # Store the current timestamp as date_modified
        )
        
        return redirect('serviceapresvente:stock')
     
    context = {
        'stock': stock,
        'page':'stock',
        'subpage':'stock_tab',
    }
    
    return render(request, 'servicedsi/index.html', context)

@login_required
def delete_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    if request.method == 'POST':
        product_name = stock.stock_produit.name  # Store the product name for the log
        stock.delete()
        return redirect('serviceapresvente:stock')
    
    ActionLog.objects.create(
            product_name=product_name,
            action_done_by=request.user.username,
            date_deleted=timezone.now()  # Store the current timestamp as date_deleted
    )
    context = {
        'page':'stock',
        'subpage':'stock_tab',
    }
    
    return render(request, 'servicedsi/index.html', context)




