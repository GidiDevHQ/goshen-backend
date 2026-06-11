from django.contrib import admin

from .models import(
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

# ─── PRODUCT IMAGE INLINE ───
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    
# ─── ORDER ITEM INLINE ───
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price', 'subtotal']

# ─── BRAND ADMIN ───
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    
# ─── CATEGORY ADMIN ───
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    
# ─── PRODUCT ADMIN ───
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'price', 'discount_price', 'in_stock', 'is_featured']
    list_display_links = ['name']
    list_editable = ['in_stock', 'is_featured']
    list_filter = ['brand', 'category', 'in_stock', 'is_featured']
    search_fields = ['name', 'description']
    inlines = [ProductImageInline]
    
# ─── PROMO CODE ADMIN ───
@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'expiry_date', 'is_active']
    list_filter = ['is_active']
    search_fields = ['code']
    
# ─── CUSTOMER ADMIN ───
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'created_at']
    search_fields = ['user_email', 'phone']
    
# ─── ORDER ADMIN ───
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'total', 'created_at']
    list_filter = ['status']
    list_display_links = ['id', 'customer']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]
    search_fields = ['customer__user__email']
    
# ─── NOTIFICATION ADMIN ───
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['order', 'message', 'sent_at']
    readonly_fields = ['order', 'message', 'sent_at']