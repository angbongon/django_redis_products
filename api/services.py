import redis
import requests
from datetime import timedelta

from django.conf import settings

from api.models import Order, Quantity


class OrderService:
    def create(self, validated_data):
        instance, quantities = self._update_instance_related(validated_data)

        Quantity.objects.bulk_create(quantities)

        return instance

    def update(self, instance, validated_data):
        _, quantities = self._update_instance_related(validated_data, instance)
        self._update_instance(instance, validated_data)

        Quantity.objects.bulk_update_or_create(
            quantities, ['quantity'], match_field=['order', 'product'])

        return instance

    def _get_shipping_costs(self):
        try:
            redis_client = redis.Redis(
                host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
            shipping_costs = redis_client.get('shipping_costs')

            if shipping_costs is None:
                headers = {'auth': settings.SHIPPING_COSTS_KEY,
                           'Content-Type': 'application/json'}
                body = {'min': 1.00, 'max': 100.00, 'records': 1}

                shipping_costs = requests.post(
                    settings.SHIPPING_COSTS_URL, json=body, headers=headers).json().get('number')

                redis_client.set('shipping_costs', shipping_costs)
                redis_client.expire('shipping_costs', timedelta(
                    seconds=60))

            return float(shipping_costs)
        except:
            return 0.0

    def _update_instance_related(self, validated_data, instance=None):
        products_data = validated_data.pop('order_to_product', [])

        if not instance:
            shipping_costs = self._get_shipping_costs()
            validated_data['shipping_costs'] = shipping_costs
            instance = Order.objects.create(**validated_data)

        quantities = []
        instance_total_price = instance.shipping_costs

        for product_data in products_data:
            product = product_data.pop('product')

            quantity = Quantity(
                order=instance, product=product, **product_data)
            quantities.append(quantity)

            instance_total_price += product.price * quantity.quantity

        instance.total_price = instance_total_price
        instance.save()

        return instance, quantities

    def _update_instance(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
