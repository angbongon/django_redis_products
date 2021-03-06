from rest_framework import serializers

from api import models
from api.services import OrderService


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class QuantityDefaultSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = models.Quantity
        fields = ['product', 'quantity']


class QuantityCreateOrUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Quantity
        fields = ['product', 'quantity']


class OrderDefaultSerializer(serializers.ModelSerializer):
    products = QuantityDefaultSerializer(
        many=True, source='order_to_product', read_only=True)
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = models.Order
        fields = '__all__'


class OrderCreateOrUpdateSerializer(serializers.ModelSerializer):
    products = QuantityCreateOrUpdateSerializer(
        many=True, source='order_to_product')
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = models.Order
        fields = '__all__'
        read_only_fields = ['total_price', 'shipping_costs']

    def create(self, validated_data):
        current_user = self.context.get('request', None).user
        validated_data['user'] = current_user
        return OrderService().create(validated_data)

    def update(self, instance, validated_data):
        return OrderService().update(instance, validated_data)

    def to_representation(self, instance):
        return OrderDefaultSerializer(instance).data
