from rest_framework.routers import DefaultRouter

from apps.shop.api.api import *
from apps.serviceapresvente.api.instance.api import *
from apps.serviceapresvente.api.sav_api.api import *


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

#instance
router.register('instances', InstanceViewSet, basename='instance')
router.register('instance-recouvrements', InstanceRecouvrementViewSet, basename='instance-recouvrement')


#service apres vente
router.register('sav_request', SavRequestViewSet)
router.register(r'commandesav', CommandeSavViewSet)
router.register(r'assemblagereparation', AssemblageReparationViewSet, basename='assemblagereparation')
router.register(r'suivicommandesav', SuiviCommandeSavViewSet, basename='suivicommandesav')
router.register(r'recouvrements', RecouvrementViewSet)
router.register(r'livraisonclient', LivraisonClientViewSet, basename='livraisonclient')




#personnel
router.register(r'personnels', PersonnelsViewSet)

#partenaire
router.register(r'partenaires', PartenairesViewSet)


urlpatterns = router.urls
