from django.contrib import admin
from product.models import Category, Product, Cart, CartItem, Order
from django.conf import settings

User = settings.AUTH_USER_MODEL

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price','items', 'created_at')  # Display user
    search_fields = ('user__username',)  # Allow searching by username


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)


