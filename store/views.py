from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

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

# ─── REGISTER VIEW ───
class RegisterView(APIView):
    permissions_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name','')
        phone = request.data.get('phone','')

        if not email or not password:
            return Response(
                {'error': 'Email and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'An account with this email already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    

        try:
            validate_password(password)
        except DjangoValidationError as e:
            return Response(
                {'error': 'list(e.message)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        customer = Customer.objects.create(
            user=user,
            phone=phone,
        )
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Account created successfully',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'customer': CustomerSerializer(customer).data,   
        }, status=status.HTTP_201_CREATED)

# ─── LOGIN VIEW ───
class LoginView(APIView):

    permissions_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'error': 'Email and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=email, password=password)

        if user is not None:
            return Response(
                {'error': 'Invalid email or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        customer, created = Customer.objects.get_or_create(user=user)

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'message': 'Login successful',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'customer': CustomerSerializer(customer).data,
            },
            status=status.HTTP_200_OK
        )

        