from apps.shop.models.Setting import Setting
from apps.shop.models.Social import Social
from apps.shop.models.Page import Page
from apps.shop.models.Category import Category
from apps.shop.models.NavCollection import NavCollection
from apps.shop.services.cart_service import CartService

def site_settings(request):
  site_settings = Setting.objects.first()
  social_settings = Social.objects.all()
  head_pages = Page.objects.filter(is_head=True)
  foot_pages = Page.objects.filter(is_foot=True)
  checkout_pages = Page.objects.filter(is_checkout=True)
  mega_categories = Category.objects.filter(is_mega=True)
  navcollections = NavCollection.objects.all()[:3]
  cart_data = CartService.get_cart_details(request)
  
  my_head_pages = []
  my_foot_pages = []
  my_checkout_pages = []
  my_socials = []
  my_mega_categories = []
  my_navcollection = []

  for nav_item in navcollections:
      my_navcollection.append({
        'title': nav_item.title,
        'description': nav_item.description,
        'button_text': nav_item.button_text,
        'button_link': nav_item.button_link,
        'imageUrl': nav_item.image.url,
      })
      
  
  for item in social_settings:
    my_socials.append({
      'name':item.name,
      'icon':item.icon,
      'link':item.link,
    })
  for item in head_pages:
    my_head_pages.append({
      'name':item.name,
      'slug':item.slug,
    })   
  for item in foot_pages:
      my_foot_pages.append({
      'name':item.name,
      'slug':item.slug,
    })   
  for item in checkout_pages:
      my_checkout_pages.append({
      'name':item.name,
      'slug':item.slug,
    })        
  for category in mega_categories:
      products = category.product_set.all()[:4]
      product_arr = []

      for product in products:
        image = None
        if product.images.exists():
          image_obj = product.images.first()
          image = image_obj.image.url
        product_arr.append({
          'name':product.name,
          'slug':product.slug,
          'image':image
        })
            
      my_mega_categories.append({
        'name':category.name,
        'product':product_arr,
      })     
  context = {
      'name':site_settings.name,
      'description':site_settings.description,
      'email':site_settings.email,
      'phone':site_settings.phone,
      'street':site_settings.street,
      'city':site_settings.city,
      'code_postal':site_settings.code_postal,
      'state':site_settings.state,
      'copyright':site_settings.copyright,
      'socials':my_socials,
      'head_pages':my_head_pages,
      'foot_pages':my_foot_pages,
      'checkout_pages':my_checkout_pages,
      'my_mega_categories':my_mega_categories,
      'my_navcollection':my_navcollection,
      'cart_data':cart_data,
  }
  request.session.update(context)

  return context