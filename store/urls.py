from rest_framework.routers import DefaultRouter

from store.models import Order

from .views import (
    BrandViewSet,
    CategoryViewSet,
    ProductViewSet,
    PromoCodeViewSet,
    CustomerViewSet,
    OrderViewSet,
    NotificationViewSet,
)

router = DefaultRouter()
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'promocodes', PromoCodeViewSet, basename='promocode')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = router.urls