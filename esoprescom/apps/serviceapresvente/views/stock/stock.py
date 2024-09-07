from apps.shop.models.Product import Stock, Product
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone

@login_required
def stock(request):
    
    #write your code logic here
    stocks = Stock.objects.all().select_related('stock_produit')
    products = Product.objects.exclude(stock__isnull=False)

    
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
        stock.delete()
        return redirect('serviceapresvente:stock')
    
    context = {
        'page':'stock',
        'subpage':'stock_tab',
    }
    
    return render(request, 'servicedsi/index.html', context)




