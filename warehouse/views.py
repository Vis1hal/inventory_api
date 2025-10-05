from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_update(self, serializer):
        if 'stock_quantity' in serializer.validated_data:
            if serializer.validated_data['stock_quantity'] < 0:
                raise serializer.ValidationError({"stock_quantity": "Cannot be negative."})
        serializer.save()

    @action(detail=True, methods=['post'])
    def add_stock(self, request, pk=None):
        product = self.get_object()
        quantity = request.data.get('quantity')
        if not quantity or not isinstance(quantity, int) or quantity <= 0:
            return Response({"error": "Quantity must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)
        
        product.stock_quantity += quantity
        product.save()
        return Response(ProductSerializer(product).data)

    @action(detail=True, methods=['post'])
    def remove_stock(self, request, pk=None):
        product = self.get_object()
        quantity = request.data.get('quantity')
        if not quantity or not isinstance(quantity, int) or quantity <= 0:
            return Response({"error": "Quantity must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)
        
        if product.stock_quantity < quantity:
            return Response({"error": "Insufficient stock available."}, status=status.HTTP_400_BAD_REQUEST)
        
        product.stock_quantity -= quantity
        product.save()
        return Response(ProductSerializer(product).data)

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        low_stock_products = Product.objects.filter(stock_quantity__lt=Product.F('low_stock_threshold'))
        serializer = self.get_serializer(low_stock_products, many=True)
        return Response(serializer.data)