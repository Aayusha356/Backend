from rest_framework import serializers
from rest_framework.fields import CharField
from django.conf import settings  # ✅ For referencing CustomUser
from .models import Product, Category, Cart, CartItem, Order

User = settings.AUTH_USER_MODEL  # ✅ Get the CustomUser model dynamically

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    image_url = CharField(source='image.url', read_only=True)
    # Override the category field to return its name instead of its id
    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = serializers.JSONField()  # ✅ Items stored as JSON
    user = serializers.CharField(source='user.username', read_only=True)  # ✅ Replace customer with user

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'total_price', 'items']
