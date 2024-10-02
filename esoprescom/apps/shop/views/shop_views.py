from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.urls import reverse
from apps.shop.models.Page import Page
from apps.shop.models.Slider import Slider
from apps.shop.models.Collection import Collection
from apps.shop.models.Product import Product
from apps.shop.models.Category import Category
from apps.shop.models.Setting import Setting
from django.http import JsonResponse


# def index(request):
#    sliders = Slider.objects.all()
#    collections = Collection.objects.all()
#    best_sellers = Product.objects.filter(is_best_seller=True)
#    new_arrival = Product.objects.filter(is_new_arrival=True)
#    featured = Product.objects.filter(is_featured=True)
#    special_offer = Product.objects.filter(is_special_offer=True)
      
#    return render(request,'shop/index.html',{'sliders':sliders,
#                                           'collections':collections,
#                                           'best_sellers':best_sellers,
#                                           'new_arrival':new_arrival,
#                                           'featured':featured,
#                                           'special_offer':special_offer,})

def index(request):
    sliders = Slider.objects.all()
    collections = Collection.objects.all()

    # Fetching all products and applying filters
    best_sellers = Product.objects.filter(is_best_seller=True)
    new_arrival = Product.objects.filter(is_new_arrival=True)
    featured = Product.objects.filter(is_featured=True)
    special_offer = Product.objects.filter(is_special_offer=True)

    # Pagination
    def get_paginated_products(products, page_number):
        paginator = Paginator(products, 20)  # Show 20 products per page
        return paginator.get_page(page_number)

    new_arrival_page = get_paginated_products(new_arrival, request.GET.get('page_new_arrival', 1))
    best_sellers_page = get_paginated_products(best_sellers, request.GET.get('page_best_sellers', 1))
    featured_page = get_paginated_products(featured, request.GET.get('page_featured', 1))
    special_offer_page = get_paginated_products(special_offer, request.GET.get('page_special_offer', 1))

    return render(request, 'shop/index.html', {
        'sliders': sliders,
        'collections': collections,
        'best_sellers': best_sellers_page,
        'new_arrival': new_arrival_page,
        'featured': featured_page,
        'special_offer': special_offer_page,
    })

def display_page(request,slug):
   page = get_object_or_404(Page,slug=slug)
      
   return render(request,'shop/page.html',{'page':page,})



def display_product(request,slug):
   product = get_object_or_404(Product,slug=slug)
      
   return render(request,'shop/single_product.html',{'product':product,})



def shop(request):
   products = Product.objects.all()
   categories = Category.objects.all()
   page = request.GET.get('page',1)
   showing = int(request.session.get('showing',6))
   sort_by_price = request.session.get('sort-price','asc')

   if 'sort-price' in request.GET and request.GET['sort-price'] != "":
       sort_by_price = request.GET['sort-price']
       request.session['sort-price'] = sort_by_price
       
   if 'showing' in request.GET and request.GET['showing'] != "":
       showing = request.GET['showing']
       request.session['showing'] = showing
       
   if sort_by_price == "asc":
      products = products.order_by('solde_price')
   elif sort_by_price == "desc":
      products = products.order_by('-solde_price')

   category_id = request.GET.get('category_id','all')
   #print('category_id:',category_id)
   if category_id and category_id != 'all':
      category = get_object_or_404(Category,id=category_id)
      products = category.product_set.all()
   else:
      products = Product.objects.all()
      
   display = request.session.get('display','grid')
   paginator  = Paginator(products,showing)
       
   #display = request.GET.get('display','grid')
   if 'display' in request.GET:
       display = request.GET['display']
       request.session['display'] = display

   try:
       products_page = paginator.page(page)
   except PageNotAnInteger:
       products_page = paginator.page(1)
   except EmptyPage:
       products_page = paginator.page(paginator.num_pages)
   except :
       products_page = paginator.page(1)    
   
   
   return render(request,'shop/shop_list.html',
                 {'products':products_page,
                  'display':display,
                  'sort_by_price':sort_by_price,
                  'categories':categories,
                  'default_category_id':int(category_id) if category_id.isdigit() else category_id,
                  })
   
   
   

def search_products(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(name__icontains=query)  # Adjust filter as needed
        products_data = [
            {
                'id': product.id,
                'name': product.name,
                'slug': product.slug,
                'solde_price': product.solde_price,
                'regular_price': product.regular_price,
                'description': product.description,
                'image': product.images.first().image.url if product.images.exists() else '',  # Assuming Product has a related images model
                'url': reverse('shop:single_product', kwargs={'slug': product.slug}),
                'add_to_cart_url': reverse('shop:add_to_cart', kwargs={'product_id': product.id}),
                'add_to_compare_url': reverse('shop:add_to_compare', kwargs={'product_id': product.id}),
                'add_to_wishlist_url': reverse('shop:add_to_wishlist', kwargs={'product_id': product.id}),
                'is_best_seller': product.is_best_seller,  # Include additional product properties if needed
                'is_new_arrival': product.is_new_arrival,
                'is_featured': product.is_featured,
                'is_special_offer': product.is_special_offer,
            } for product in products
        ]
    else:
        products_data = []

    return JsonResponse({'products': products_data})

