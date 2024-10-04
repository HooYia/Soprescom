from django.utils import timezone
import logging

from apps.shop.models.Product import ActionLog, Stock, Product, Category
from django.shortcuts import render, get_object_or_404

from django.contrib import messages
from django.db import transaction
from apps.shop.models.Image import Image
from django.utils.translation import gettext as _


from django.utils.text import slugify
from load_task_in_production import search_serpapi_images, save_images_for_product

from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)



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

@login_required
def product_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        reference = request.POST.get('reference')
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
                        reference=reference,
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
                    print("product:",product.name)
                    
                    

                    # Fetch and save images using search_serpapi_images
                    result = search_serpapi_images(name, name)  # Use name as both reference and designation here
                    print("result:",result)
                    if result['images_url']:
                        save_images_for_product(product, result['images_url'], name)

                    
                    # Create an action log for the product creation
                    ActionLog.objects.create(
                        product_name=product.name,
                        date_created=timezone.now(),
                        action_done_by=request.user.username,  # Assuming you're using the username of the logged-in user
                        type = 'product',
                        
                    )
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
                    product.reference = reference
                    product.save()
                    product.categories.set(category_ids)  # Update categories for the existing product
                    
                    ActionLog.objects.create(
                        product_name=product.name,
                        action_done_by=request.user.username,
                        date_modified=timezone.now(),  # Store the current timestamp as date_modified
                        type = 'product',
                        
                    )

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
                    product_name = product.name
                    product.delete()
                    
                    ActionLog.objects.create(
                        product_name=product_name,
                        action_done_by=request.user.username,
                        date_deleted=timezone.now(),  # Store the current timestamp as date_deleted
                        type = 'product',
                        
                    )
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
