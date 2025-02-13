from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings  # ✅ For referencing CustomUser
from .models import Product, Category, Cart, CartItem, Order
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, CartItemSerializer, OrderSerializer

User = settings.AUTH_USER_MODEL  # ✅ Get the CustomUser model dynamically

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print("Incoming request data:", request.data) 
        # ✅ Fetch the logged-in user instead of Customer
        user = request.user

        # Get the items and total price from the request data
        items = request.data.get('items', [])
        if not items:
            return Response({"detail": "Items are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate total price and handle type conversions for each item
        total_price_value = 0
        item_data = []

        for item in items:
            try:
                # Convert price and quantity to correct types
                product = Product.objects.get(id=int(item["id"]))  # Fetch product by ID
                quantity = int(item["quantity"])  # Ensure quantity is an integer
                size = item["size"]
                price = float(item["price"])  # Convert price to float
                total_price_value += price * quantity  # Calculating total price

                # Add the item details
                item_data.append({
                    "product_id": product.id,
                    "quantity": quantity,
                    "size": size,
                    "price": price,
                    "name": product.name,
                    "image": item.get("image", ""),  # Optional image field
                })
            except ValueError:
                return Response({"detail": "Invalid data format for price or quantity."}, status=status.HTTP_400_BAD_REQUEST)
            except Product.DoesNotExist:
                return Response({"detail": f"Product with ID {item['id']} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Create the order with the logged-in user instead of Customer
        order = Order.objects.create(
            user=user,
            total_price=total_price_value,
            items=item_data
        )

        # Serialize the created order and return the response
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
