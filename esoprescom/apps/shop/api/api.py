from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from apps.shop.models import *
from apps.shop.api.serializers import *

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.shop.services.cart_service import CartService
from apps.shop.models import Carrier, Product
from apps.shop.services.compare_service import CompareService
from apps.shop.services.wish_service import WishService
from apps.shop.services.payment_service import StripeService
from apps.shop.views.checkout_views import create_order
from apps.dashboard.models.Address import Address

import stripe

from apps.shop.services.payment_service import StripeService




class CategoryViewSet(viewsets.ModelViewSet):
    """
    Name: CategoryViewSet
    Description: CRUD operations for the Category model.
    Author: fotsingtchoupe1@gmail.com
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    Name: ProductViewSet
    Description: CRUD operations for Product model.
    Author: fotsingtchoupe1@gmail.com
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    # permission_classes = [IsAuthenticatedOrReadOnly]



class CartViewSet(viewsets.ViewSet):
    """
    Name: CartViewSet
    Description: Handles cart operations including adding/removing items, and retrieving cart details.
    Author: fotsingtchoupe1@gmail.com
    """
    
    def list(self, request):
        """
        Retrieve the details of the cart.
        """
        cart = CartService.get_cart_details(request)
        if not cart['items']:
            return Response({"detail": "Cart is empty."}, status=status.HTTP_204_NO_CONTENT)
        
        serializer = CartDetailSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='add/(?P<product_id>\d+)')
    def add_to_cart(self, request, product_id):
        """
        Add a product to the cart.
        """
        CartService.add_to_cart(request, product_id, 1)
        return Response({"detail": "Product added to cart."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='remove/(?P<product_id>\d+)/(?P<quantity>\d+)')
    def remove_from_cart(self, request, product_id, quantity):
        """
        Remove a product from the cart or decrease its quantity.
        """
        CartService.remove_from_cart(request, product_id, int(quantity))
        return Response({"detail": "Product removed from cart."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='clear')
    def clear_cart(self, request):
        """
        Clear the entire cart.
        """
        CartService.clear_cart(request)
        return Response({"detail": "Cart cleared."}, status=status.HTTP_200_OK)



class CompareViewSet(viewsets.ViewSet):
    """
    Name: CompareViewSet
    Description: Handles operations related to product comparison, including adding/removing products, and retrieving compared product details.
    Author: fotsingtchoupe1@gmail.com
    """
    
    def list(self, request):
        """
        Retrieve the list of compared products with their details.
        """
        compare = CompareService.get_compared_products_details(request)
        if not compare:
            return Response({"detail": "No products in compare list."}, status=status.HTTP_204_NO_CONTENT)
        
        serializer = CompareProductSerializer(compare, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='add/(?P<product_id>\d+)')
    def add_to_compare(self, request, product_id):
        """
        Add a product to the compare list.
        """
        CompareService.add_product_to_compare(request, product_id)
        return Response({"detail": "Product added to compare list."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='remove/(?P<product_id>\d+)')
    def remove_from_compare(self, request, product_id):
        """
        Remove a product from the compare list.
        """
        CompareService.remove_product_from_compare(request, product_id)
        return Response({"detail": "Product removed from compare list."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='clear')
    def clear_compare(self, request):
        """
        Clear the entire compare list.
        """
        CompareService.clear_compared_products(request)
        return Response({"detail": "Compare list cleared."}, status=status.HTTP_200_OK)




class WishlistViewSet(viewsets.ViewSet):
    """
    Name: WishlistViewSet
    Description: Handles operations related to product wishlists, including adding/removing products and retrieving wished product details.
    Author: fotsingtchoupe1@gmail.com
    """
    
    def list(self, request):
        """
        Retrieve the list of wished products with their details.
        """
        wishlist = WishService.get_wished_products_details(request)
        if not wishlist:
            return Response({"detail": "No products in wishlist."}, status=status.HTTP_204_NO_CONTENT)
        
        serializer = WishProductSerializer(wishlist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='add/(?P<product_id>\d+)')
    def add_to_wishlist(self, request, product_id):
        """
        Add a product to the wishlist.
        """
        WishService.add_product_to_wish(request, product_id)
        return Response({"detail": "Product added to wishlist."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='remove/(?P<product_id>\d+)')
    def remove_from_wishlist(self, request, product_id):
        """
        Remove a product from the wishlist.
        """
        WishService.remove_product_from_wish(request, product_id)
        return Response({"detail": "Product removed from wishlist."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='clear')
    def clear_wishlist(self, request):
        """
        Clear the entire wishlist.
        """
        WishService.clear_wished_products(request)
        return Response({"detail": "Wishlist cleared."}, status=status.HTTP_200_OK)



class OrderViewSet(viewsets.ViewSet):
    """
    Name: OrderViewSet
    Description: Handles order creation and retrieval.
    Author: fotsingtchoupe1@gmail.com
    """
    
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """
        Create a new order.
        """
        user = request.user
        cart = CartService.get_cart_details(request)
        carrier = request.session.get('carrier', {})
        billing_address = request.data.get('billing_address', '')
        shipping_address = request.data.get('shipping_address', billing_address)
        payment_method = 'Stripe'

        order = Order(
            client_name=user.username,
            billing_address=billing_address,
            shipping_address=shipping_address,
            carrier_name=carrier.get('name', 'Unknown'),
            carrier_price=carrier.get('price', 0.0),
            quantity=cart['cart_count'],
            order_cost=cart['sub_total_ht'],
            taxe=cart['taxe_amount'],
            order_cost_ttc=cart['sub_total_with_shipping'],
            payment_method=payment_method,
            author=user
        )
        order.save()

        # Order details
        for item in cart['items']:
            Orderdetails.objects.create(
                product_name=item['product']['name'],
                product_description=item['product']['description'],
                solde_price=item['product']['solde_price'],
                regular_price=item['product']['regular_price'],
                quantity=item['quantity'],
                taxe=item['taxe_amount'],
                sub_total_ht=item['sub_total_ht'],
                sub_total_ttc=item['sub_total_ttc'],
                order=order
            )

        return Response({'order_id': order.id}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific order by ID.
        """
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddressViewSet(viewsets.ModelViewSet):
    """
    Name: AddressViewSet
    Description: Handles CRUD operations for addresses.
    Author: fotsingtchoupe1@gmail.com
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class CheckoutViewSet(viewsets.ViewSet):
    """
    Name: CheckoutViewSet
    Description: Handles checkout operations.
    Author: fotsingtchoupe1@gmail.com
    """
    
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def checkout(self, request):
        """
        Retrieve the checkout details, including carriers and payment information.
        """
        carrier_id = request.GET.get('carrier_id')
        address_billing_id = request.GET.get('address_billing_id', '')
        address_shipping_id = request.GET.get('address_shipping_id', address_billing_id)
        new_shipping_address = request.GET.get('new_shipping_address', '')

        ready_to_pay = bool(address_billing_id) and (new_shipping_address or address_shipping_id)

        if carrier_id:
            carrier = Carrier.objects.filter(id=carrier_id).first()
            if carrier:
                request.session['carrier'] = {
                    'id': carrier.id,
                    'name': carrier.name,
                    'price': carrier.price
                }

        cart = CartService.get_cart_details(request)
        order_id = None

        if ready_to_pay:
            # Create order
            if new_shipping_address and new_shipping_address != 'false':
                billing_address = Address.objects.filter(id=address_billing_id).first()
                shipping_address = Address.objects.filter(id=address_shipping_id).first()
            else:
                billing_address = Address.objects.filter(id=address_billing_id).first()
                shipping_address = None

            billing_address_str = billing_address.get_address_as_string() if billing_address else ""
            shipping_address_str = shipping_address.get_address_as_string() if shipping_address else ""
            order_id = create_order(request, billing_address_str, shipping_address_str)

        payment_service = StripeService()
        carriers = Carrier.objects.all()

        return Response({
            'cart': cart,
            'carriers': [carrier.name for carrier in carriers],
            'address_form': AddressSerializer().data,  # For frontend to use
            'ready_to_pay': ready_to_pay,
            'address_billing_id': address_billing_id,
            'address_shipping_id': address_shipping_id,
            'new_shipping_address': new_shipping_address,
            'order_id': order_id,
            'public_key': payment_service.get_public_key,
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def add_address(self, request):
        """
        Add a new address for the user.
        """
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            address = serializer.save(author=request.user)
            return Response({'message': 'Address added successfully'}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class PaymentViewSet(viewsets.ViewSet):
    """
    Name: PaymentViewSet
    Description: Handles payment operations including creating payment intents and handling payment success.
    Author: fotsingtchoupe1@gmail.com
    """
    
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def create_payment_intent(self, request):
        """
        Create a Stripe PaymentIntent for the given order.
        """
        order_id = request.data.get('order_id')
        if not order_id:
            return Response({'error': 'Order ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        order = get_object_or_404(Order, pk=order_id)
        payment_service = StripeService()
        stripe.api_key = payment_service.get_private_key()

        try:
            amount = int(order.order_cost_ttc * 100)  # Stripe requires amount in cents
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='eur',
                automatic_payment_methods={'enabled': True},
            )
            order.strip_payment_intent = payment_intent['id']
            order.save()

            return Response({
                'clientSecret': payment_intent['client_secret']
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def payment_success(self, request):
        """
        Handle the success of a payment and update the order status.
        """
        payment_intent_id = request.GET.get('payment_intent')
        if not payment_intent_id:
            return Response({'error': 'Payment Intent ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        payment_service = StripeService()
        stripe.api_key = payment_service.get_private_key()

        try:
            payment = stripe.PaymentIntent.retrieve(payment_intent_id)
            if payment.status == 'succeeded':
                order = get_object_or_404(Order, strip_payment_intent=payment_intent_id)
                order.is_paid = True
                order.save()
                return Response({'message': 'Payment succeeded'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Payment not successful'}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
