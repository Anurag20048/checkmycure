from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Category, Product, Customer, Order, OrderItem
from .serializers import (
    CategorySerializer, ProductSerializer, CustomerSerializer, 
    OrderSerializer, OrderCreateSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for categories
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """Get all products in a category"""
        category = self.get_object()
        products = category.products.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for products
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category', None)
        is_active = self.request.query_params.get('is_active', None)
        
        if category is not None:
            queryset = queryset.filter(category_id=category)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset

    @action(detail=True, methods=['post'])
    def update_stock(self, request, pk=None):
        """Update product stock"""
        product = self.get_object()
        stock = request.data.get('stock')
        
        if stock is not None:
            product.stock = stock
            product.save()
            return Response({'status': 'stock updated', 'stock': product.stock})
        else:
            return Response({'error': 'stock field is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)


class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for customers
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=True, methods=['get'])
    def orders(self, request, pk=None):
        """Get all orders for a customer"""
        customer = self.get_object()
        orders = customer.orders.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for orders
    """
    queryset = Order.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.all()
        customer = self.request.query_params.get('customer', None)
        status_filter = self.request.query_params.get('status', None)
        
        if customer is not None:
            queryset = queryset.filter(customer_id=customer)
        if status_filter is not None:
            queryset = queryset.filter(status=status_filter)
        
        return queryset

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update order status"""
        order = self.get_object()
        new_status = request.data.get('status')
        
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            return Response({'status': 'order status updated', 'new_status': order.status})
        else:
            return Response({'error': 'invalid status'}, 
                          status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def admin_login(request):
    """
    Admin login using Django admin credentials
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Authenticate using Django authentication
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response(
            {'error': 'Invalid admin credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Check if user is staff/admin
    if not user.is_staff and not user.is_superuser:
        return Response(
            {'error': 'Access denied. Admin privileges required.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Get or create token
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser
        }
    })

# Emergency endpoints are now in the 'emergency' app
