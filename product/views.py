from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product, Category, Customer, Cart, CartItem, Order
from .serializers import ProductSerializer, CategorySerializer, CustomerSerializer, CartSerializer, CartItemSerializer, OrderSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Fetch the customer instance (logged-in user)
        customer_instance = Customer.objects.get(id=request.user.id)
        
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
                product = Product.objects.get(id=int(item["id"]))  # Fetch product by id
                quantity = int(item["quantity"])  # Ensure quantity is an integer
                size = item["size"]
                price = float(item["price"])  # Convert price to float or Decimal
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

        # Now create the order
        order_data = {
            "customer": customer_instance,
            "total_price": total_price_value,
            "items": item_data
        }

        # Create the order
        order = Order.objects.create(**order_data)

        # Serialize the created order and return the response
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
