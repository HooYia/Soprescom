from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from shop.models.Page import Page
from shop.models.Slider import Slider
from shop.models.Collection import Collection
from shop.models.Product import Product
from shop.models.Category import Category
from shop.models.Setting import Setting

def index(request):
   sliders = Slider.objects.all()
   collections = Collection.objects.all()
   best_sellers = Product.objects.filter(is_best_seller=True)
   new_arrival = Product.objects.filter(is_new_arrival=True)
   featured = Product.objects.filter(is_featured=True)
   special_offer = Product.objects.filter(is_special_offer=True)
      
   return render(request,'shop/index.html',{'sliders':sliders,
                                          'collections':collections,
                                          'best_sellers':best_sellers,
                                          'new_arrival':new_arrival,
                                          'featured':featured,
                                          'special_offer':special_offer,})


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