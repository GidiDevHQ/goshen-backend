from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


from .models import (
    Brand,
    Category,
    Product,
    PromoCode,
    Customer,
    Order,
    Notification,
)

from .serializers import (
    BrandSerializer,
    CategorySerializer,
    ProductSerializer,
    PromoCodeSerializer,
    CustomerSerializer,
    OrderSerializer,
    NotificationSerializer,
)

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
    
# ─── CATEGORY VIEWSET ───
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
    
# ─── PRODUCT VIEWSET ───
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'featured', 'by_brand', 'by_category']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        queryset = Product.objects.all()
        
        brand = self.request.query_params.get('brand')
        if brand:
            queryset = queryset.filter(brand__id=brand)
            
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__id=category)
            
        in_stock = self.request.query_params.get('in_stock')
        if in_stock:
            queryset = queryset.filter(in_stock=True)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured = Product.objects.filter(is_featured=True)
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)
    
    
# ─── PROMO CODE VIEWSET ───
class PromoCodeViewSet(viewsets.ModelViewSet):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer
    
    @action(detail=False, methods=['post'])
    def validate(self, request):
        code = request.data.get('code')
        
        if not code:
            return Response(
                {'error': 'Please provide a promo code'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            promo = PromoCode.objects.get(code=code, is_active=True)
            serializer = self.get_serializer(promo)
            return Response(serializer.data)
        
        except PromoCode.DoesNotExist:
            return Response(
                {'error': 'Invalid or expired promo code'},
                status=status.HTTP_404_NOT_FOUND
            )
            
# ─── CUSTOMER VIEWSET ───
class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Customer.objects.all()
        return Customer.objects.filter(user=self.request.user)
    
    def get_permissions(self):
        return [IsAuthenticated()]
    
# ─── ORDER VIEWSET ───
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(customer__user=self.request.user)
    
    def get_permissions(self):
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        orders = Order.objects.filter(customer__user=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
# ─── NOTIFICATION VIEWSET ───
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    
    def get_permissions(self):
        return [IsAuthenticated()]
