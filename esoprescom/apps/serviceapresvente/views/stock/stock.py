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
from datetime import datetime, timedelta


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
            date_created=timezone.now(),  # Store the current timestamp as date_created
            type = 'stock',
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
            date_modified=timezone.now(),  # Store the current timestamp as date_modified
            type = 'stock',
            
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
            date_deleted=timezone.now(),  # Store the current timestamp as date_deleted
            type = 'stock',
            
    )
    context = {
        'page':'stock',
        'subpage':'stock_tab',
    }
    
    return render(request, 'servicedsi/index.html', context)


@login_required
def action_log(request):
    action_logs = ActionLog.objects.all()
    filter_option = request.GET.get('filter', 'all')
    today = datetime.now()

    if filter_option == 'today':
        action_logs = action_logs.filter(
            date_created__date=today
        ) | action_logs.filter(
            date_modified__date=today
        ) | action_logs.filter(
            date_deleted__date=today
        )
    elif filter_option == 'yesterday':
        yesterday = today - timedelta(days=1)
        action_logs = action_logs.filter(
            date_created__date=yesterday
        ) | action_logs.filter(
            date_modified__date=yesterday
        ) | action_logs.filter(
            date_deleted__date=yesterday
        )
    elif filter_option == 'last_7_days':
        last_7_days = today - timedelta(days=7)
        action_logs = action_logs.filter(
            date_created__date__gte=last_7_days
        ) | action_logs.filter(
            date_modified__date__gte=last_7_days
        ) | action_logs.filter(
            date_deleted__date__gte=last_7_days
        )
    elif filter_option == 'last_month':
        last_month = today - timedelta(days=30)
        action_logs = action_logs.filter(
            date_created__date__gte=last_month
        ) | action_logs.filter(
            date_modified__date__gte=last_month
        ) | action_logs.filter(
            date_deleted__date__gte=last_month
        )
    elif filter_option == 'last_year':
        last_year = today - timedelta(days=365)
        action_logs = action_logs.filter(
            date_created__date__gte=last_year
        ) | action_logs.filter(
            date_modified__date__gte=last_year
        ) | action_logs.filter(
            date_deleted__date__gte=last_year
        )
    elif filter_option == 'custom_date':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if start_date and end_date:
            action_logs = action_logs.filter(
                date_created__date__range=[start_date, end_date]
            ) | action_logs.filter(
                date_modified__date__range=[start_date, end_date]
            ) | action_logs.filter(
                date_deleted__date__range=[start_date, end_date]
            )

    context = {
        'action_logs': action_logs,
        'filter_option': filter_option,
        'page': 'stock',
        'subpage': 'log_tab',
    }
    return render(request, 'servicedsi/index.html', context)