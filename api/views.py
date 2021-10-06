from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.models import Product, Order
from api.serializers import ProductSerializer, OrderDefaultSerializer, OrderCreateOrUpdateSerializer
from api.permissions import OrderPermission


class OrderViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return an order instance.

    list:
        Return logged user's order. In case of superuser returns all orders

    create:
        Create a new order.

    delete:
        Remove an existing order.

    partial_update:
        Update one or more fields on an existing order.

    update:
        Update an order.
    """
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
    """
    retrieve:
        Return an product instance.

    list:
        Return all products

    create:
        Create a new product.

    delete:
        Remove an existing product.

    partial_update:
        Update one or more fields on an existing product.

    update:
        Update an product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
