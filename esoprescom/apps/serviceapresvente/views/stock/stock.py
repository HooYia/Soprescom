import logging

from apps.shop.models.Product import Stock, Product, Category
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from django.contrib import messages
from django.db import transaction
from apps.shop.models.Image import Image
from django.utils.translation import gettext as _


logger = logging.getLogger(__name__)

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





# def product_view(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         slug = request.POST.get('slug')
#         description = request.POST.get('description')
#         more_description = request.POST.get('more_description')
#         additional_infos = request.POST.get('additional_infos')
#         solde_price = request.POST.get('solde_price')
#         regular_price = request.POST.get('regular_price')
#         brand = request.POST.get('brand')
#         is_available = request.POST.get('is_available') == 'on'
#         is_best_seller = request.POST.get('is_best_seller') == 'on'
#         is_new_arrival = request.POST.get('is_new_arrival') == 'on'
#         is_featured = request.POST.get('is_featured') == 'on'
#         is_special_offer = request.POST.get('is_special_offer') == 'on'
#         action = request.POST.get('action')
#         product_id = request.POST.get('id')

#         # Handle selected category IDs
#         category_ids = request.POST.getlist('categories')  # Assuming your template uses 'categories' as the name for the select input

#         try:
#             with transaction.atomic():
#                 if action == 'create':
#                     product = Product(
#                         name=name,
#                         slug=slug,
#                         description=description,
#                         more_description=more_description,
#                         additional_infos=additional_infos,
#                         solde_price=solde_price,
#                         regular_price=regular_price,
#                         brand=brand,
#                         is_available=is_available,
#                         is_best_seller=is_best_seller,
#                         is_new_arrival=is_new_arrival,
#                         is_featured=is_featured,
#                         is_special_offer=is_special_offer,
#                     )
#                     product.save()
#                     product.categories.set(category_ids)  # Set the categories for the new product

#                     # Handling image uploads
#                     images = request.FILES.getlist('images')
#                     for image in images:
#                         Image.objects.create(product=product, image=image)

#                     messages.success(request, _('Product added successfully'))

#                 elif action == 'update':
#                     product = get_object_or_404(Product, id=product_id)
#                     product.name = name
#                     product.slug = slug
#                     product.description = description
#                     product.more_description = more_description
#                     product.additional_infos = additional_infos
#                     product.solde_price = solde_price
#                     product.regular_price = regular_price
#                     product.brand = brand
#                     product.is_available = is_available
#                     product.is_best_seller = is_best_seller
#                     product.is_new_arrival = is_new_arrival
#                     product.is_featured = is_featured
#                     product.is_special_offer = is_special_offer
#                     product.save()
#                     product.categories.set(category_ids)  # Update categories for the existing product

#                     # Handling image uploads during update
#                     images = request.FILES.getlist('images')  # New images uploaded
#                     for image in images:
#                         Image.objects.create(product=product, image=image)

#                     messages.success(request, _('Product updated successfully'))

#                 elif action == 'delete':
#                     product = get_object_or_404(Product, id=product_id)
#                     product.delete()
#                     messages.success(request, _('Product deleted successfully'))

#                 else:
#                     messages.error(request, _('Invalid action'))

#         except Exception as e:
#             logger.error('Error processing product: %s', e)
#             messages.error(request, _('Error processing product. Please contact support for assistance.'))


#     # Handling the GET request to show the product form
#     products = Product.objects.all()  # Retrieve all products if needed for the modal
#     categories = Category.objects.all()  # Retrieve all categories for the modal form
#     context = {
#         'products': products,
#         'categories': categories,
#         'page':'stock',
#         'subpage':'product_tab',
#     }
#     return render(request, 'servicedsi/index.html', context)    



import requests
from serpapi import GoogleSearch

def search_serpapi_images(reference, designation):
    params = {
        "engine": "google_images",  # Use the Google Images search engine
        "q": f"{reference} {designation}",  # Query string (e.g., product reference and name)
        "num": "4",  # Number of images to fetch
        "api_key": "df95d8db357af8f9d090b079b80ed0af7b6694a5f19ec8df8809d01d3f316fe6"  # Replace with your SerpAPI key
    }

    search = GoogleSearch(params)
    data = search.get_dict()
    results = {
        'images_url': [],
        'more_detail': None,
    }

    if 'images_results' in data and len(data['images_results']) > 0:
        for result in data["images_results"][:4]:  # Limit to 4 images
            results['images_url'].append(result["original"])

        # Get the link for additional product information
        if 'link' in data['images_results'][0]:
            results['more_detail'] = data['images_results'][0]['link']

    return results


from django.core.files.base import ContentFile
from apps.shop.models import Image

def save_images_for_product(product, image_urls, name):
    for index, image_url in enumerate(image_urls):
        try:
            # Fetch the image data from the URL
            response = requests.get(image_url)
            response.raise_for_status()

            # Generate a filename for the image
            file_name = f"{name}_image_{index + 1}.jpg"

            # Create an Image instance and save it
            image_instance = Image(product=product)
            image_instance.image.save(file_name, ContentFile(response.content), save=True)

            print(f"Image {file_name} saved for product: {product.name}")
        except requests.RequestException as e:
            print(f"Failed to fetch image from {image_url}: {e}")

from django.utils.text import slugify
# from load_task_in_production import search_serpapi_images, save_images_for_product

def product_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        more_description = request.POST.get('more_description')
        additional_infos = request.POST.get('additional_infos')
        solde_price = request.POST.get('solde_price')
        regular_price = request.POST.get('regular_price')
        brand = request.POST.get('brand')
        is_available = request.POST.get('is_available') == 'on'
        is_best_seller = request.POST.get('is_best_seller') == 'on'
        is_new_arrival = request.POST.get('is_new_arrival') == 'on'
        is_featured = request.POST.get('is_featured') == 'on'
        is_special_offer = request.POST.get('is_special_offer') == 'on'
        action = request.POST.get('action')
        product_id = request.POST.get('id')

        # Handle selected category IDs
        category_ids = request.POST.getlist('categories')  # Assuming your template uses 'categories' as the name for the select input
        slug = slugify(name)
        try:
            with transaction.atomic():
                if action == 'create':
                    product = Product(
                        name=name,
                        slug=slug,
                        description=description,
                        more_description=more_description,
                        additional_infos=additional_infos,
                        solde_price=solde_price,
                        regular_price=regular_price,
                        brand=brand,
                        is_available=is_available,
                        is_best_seller=is_best_seller,
                        is_new_arrival=is_new_arrival,
                        is_featured=is_featured,
                        is_special_offer=is_special_offer,
                    )
                    product.save()
                    product.categories.set(category_ids)  # Set the categories for the new product

                    # Fetch and save images using search_serpapi_images
                    result = search_serpapi_images(name, name)  # Use name as both reference and designation here
                    print("result:",result)
                    if result['images_url']:
                        save_images_for_product(product, result['images_url'], name)

                    messages.success(request, _('Product added successfully'))

                elif action == 'update':
                    product = get_object_or_404(Product, id=product_id)
                    product.name = name
                    product.description = description
                    product.more_description = more_description
                    product.additional_infos = additional_infos
                    product.solde_price = solde_price
                    product.regular_price = regular_price
                    product.brand = brand
                    product.is_available = is_available
                    product.is_best_seller = is_best_seller
                    product.is_new_arrival = is_new_arrival
                    product.is_featured = is_featured
                    product.is_special_offer = is_special_offer
                    product.save()
                    product.categories.set(category_ids)  # Update categories for the existing product

                    # Handling image uploads during update
                    images = request.FILES.getlist('images')  # New images uploaded
                    if images:
                        # Delete old images
                        product.images.all().delete()  # Assuming 'images' is a related name from Image model to Product
                        # Add new images
                        for image in images:
                            Image.objects.create(product=product, image=image)

                    messages.success(request, _('Product updated successfully'))

                elif action == 'delete':
                    product = get_object_or_404(Product, id=product_id)
                    product.delete()
                    messages.success(request, _('Product deleted successfully'))

                else:
                    messages.error(request, _('Invalid action'))

        except Exception as e:
            logger.error('Error processing product: %s', e)
            messages.error(request, _('Error processing product. Please contact support for assistance.'))

    # Handling the GET request to show the product form
    products = Product.objects.all()  # Retrieve all products if needed for the modal
    categories = Category.objects.all()  # Retrieve all categories for the modal form
    context = {
        'products': products,
        'categories': categories,
        'page': 'stock',
        'subpage': 'product_tab',
    }
    return render(request, 'servicedsi/index.html', context)
