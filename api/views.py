from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.models import Product, Order
from api.serializers import ProductSerializer, OrderDefaultSerializer, OrderCreateOrUpdateSerializer
from api.permissions import OrderPermission


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, OrderPermission]

    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(user=current_user)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return OrderCreateOrUpdateSerializer
        return OrderDefaultSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
