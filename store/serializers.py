from operator import sub
from os import read

from rest_framework import serializers

from .models import (
    Brand,
    Category,
    Product,
    ProductImage,
    PromoCode,
    Customer,
    Order,
    OrderItem,
    Notification,
)

# ─── BRAND SERIALIZER ───
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
        
# ─── CATEGORY SERIALIZER ───
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    
# ─── PRODUCT IMAGE SERIALIZER ───
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


# ─── PRODUCT SERIALIZER ───
class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(),
        source='brand',
        write_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all(),
        source='category',
        write_only=True
    )
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'brand',
            'brand_id',
            'category',
            'category_id',
            'price',
            'discount_price',
            'description',
            'in_stock',
            'is_featured',
            'images',
            'created_at',
            'updated_at',
        ]
        
# ─── PROMO CODE SERIALIZER ───
class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = '__all__'
        
# ─── CUSTOMER SERIALIZER ───
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        
# ─── ORDER ITEM SERIALIZER ───
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    subtotal = serializers.ReadOnlyField()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'subtotal']
        
# ─── ORDER SERIALIZER ───
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer = CustomerSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id',
            'customer',
            'status',
            'promo_code',
            'total',
            'items',
            'created_at',
            'updated_at',
        ]
        
    # ─── NOTIFICATION SERIALIZER ───
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'