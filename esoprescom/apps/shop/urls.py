from django.urls import path
from apps.shop.views import shop_views,cart_views,compare_views, wishlist_views, checkout_views,payment_views

app_name = 'shop'

urlpatterns = [
    path('', shop_views.index, name='home'),
    path('page/<str:slug>', shop_views.display_page, name='display_page'),
    path('product/<str:slug>', shop_views.display_product, name='single_product'),
    path('shop', shop_views.shop, name='shop_list'),
    #cart
    path('cart', cart_views.index, name='cart'),
    path('cart/add/<int:product_id>', cart_views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/<int:quantity>', cart_views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', cart_views.clear_cart, name='clear_cart'),

    # compare   
    path('compare', compare_views.index, name='compare'),
    path('compare/add/<int:product_id>', compare_views.add_to_compare, name='add_to_compare'),
    path('compare/remove/<int:product_id>', compare_views.remove_from_compare, name='remove_from_compare'),

    # whishlist  
    path('wishlist', wishlist_views.index, name='wishlist'),
    path('wishlist/add/<int:product_id>', wishlist_views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>', wishlist_views.remove_from_wishlist, name='remove_from_wishlist'),
    #checkout
    path('checkout', checkout_views.index, name='checkout'),
    path('checkout/add_address', checkout_views.add_address, name='add_address'),
    path('checkout/login_form', checkout_views.login_form, name='login_form'),
    # create-payment-intent
    path('create-payment-intent/<str:order_id>', payment_views.index, name='create-payment-intent'),
    path('payment-success', payment_views.payment_success, name='payment_succes'),
    
    # product search
    path('search_products/', shop_views.search_products, name='search_products'),
]
