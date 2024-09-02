from rest_framework.routers import DefaultRouter

from apps.shop.api.api import *
from apps.serviceapresvente.api.instance.api import *


router = DefaultRouter()

#register your end points here

# product routers
router.register('products', ProductViewSet)
router.register('categories', CategoryViewSet)
router.register('carts', CartViewSet, basename='cart')
router.register('compares', CompareViewSet, basename='compare')
router.register('wishlists', WishlistViewSet, basename='wishlist')
router.register('orders', OrderViewSet, basename='order')
router.register('checkout', CheckoutViewSet, basename='checkout')
router.register('payments', PaymentViewSet, basename='payment')
router.register('addresses', AddressViewSet, basename='addresses')
router.register('instances', InstanceViewSet, basename='instance')
router.register('instance-recouvrements', InstanceRecouvrementViewSet, basename='instance-recouvrement')



urlpatterns = router.urls
