from rest_framework import serializers
from apps.shop.models import *
from apps.accounts.models.Customer import Customer
from apps.dashboard.models import Address



class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model, includes fields and custom method to handle image URL.
    """
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'image_url', 'is_mega', 'updated_at', 'created_at']
        read_only_fields = ['id', 'slug', 'updated_at', 'created_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    """
    categories = serializers.StringRelatedField(many=True)  # Serializing categories as strings
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'more_description', 'additional_infos',
            'solde_price', 'regular_price', 'brand', 'is_available', 'is_best_seller', 
            'is_new_arrival', 'is_featured', 'is_special_offer', 'categories', 'updated_at', 
            'created_at'
        ]
        read_only_fields = ['id', 'updated_at', 'created_at']



class CartItemSerializer(serializers.Serializer):
    """
    Serializer for individual cart items.
    """
    product = serializers.SerializerMethodField()
    quantity = serializers.IntegerField()
    sub_total = serializers.FloatField()
    taxe_amount = serializers.FloatField()
    sub_total_ht = serializers.FloatField()
    sub_total_ttc = serializers.FloatField()

    def get_product(self, obj):
        product = obj['product']
        return {
            'id': product['id'],
            'name': product['name'],
            'slug': product['slug'],
            'description': product['description'],
            'image': product['image'],
            'solde_price': product['solde_price'],
            'regular_price': product['regular_price'],
        }



class CartDetailSerializer(serializers.Serializer):
    """
    Serializer for the entire cart, including items and summary details.
    """
    items = CartItemSerializer(many=True)
    sub_total = serializers.FloatField()
    carrier_id = serializers.IntegerField()
    carrier_name = serializers.CharField()
    shipping_price = serializers.FloatField()
    taxe_amount = serializers.FloatField()
    sub_total_ht = serializers.FloatField()
    sub_total_ttc = serializers.FloatField()
    sub_total_with_shipping = serializers.FloatField()
    cart_count = serializers.IntegerField()



class CompareProductSerializer(serializers.Serializer):
    """
    Serializer for individual compared products.
    """
    id = serializers.IntegerField()
    slug = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    solde_price = serializers.FloatField()
    regular_price = serializers.FloatField()
    stock = serializers.IntegerField()
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj['images'].exists():
            return obj['images'].first().image.url
        return None



class WishProductSerializer(serializers.Serializer):
    """
    Serializer for individual wished products.
    """
    id = serializers.IntegerField()
    slug = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    solde_price = serializers.FloatField()
    regular_price = serializers.FloatField()
    stock = serializers.IntegerField()
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj['images'].exists():
            return obj['images'].first().image.url
        return None



class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orderdetails
        fields = [
            'product_name',
            'product_description',
            'solde_price',
            'regular_price',
            'quantity',
            'taxe',
            'sub_total_ht',
            'sub_total_ttc'
        ]

class OrderSerializer(serializers.ModelSerializer):
    order_details = OrderDetailsSerializer(many=True, read_only=True)
    author = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta:
        model = Order
        fields = [
            'id',
            'client_name',
            'billing_address',
            'shipping_address',
            'quantity',
            'taxe',
            'order_cost',
            'order_cost_ttc',
            'is_paid',
            'carrier_name',
            'carrier_price',
            'payment_method',
            'strip_payment_intent',
            'status',
            'updated_at',
            'created_at',
            'author',
            'order_details'
        ]



class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'name', 'full_name', 'street', 'code_postal', 
            'city', 'country', 'more_details', 'address_type'
        ]
