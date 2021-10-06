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

    def _update_instance_related(self, validated_data, instance=None):
        products_data = validated_data.pop('order_to_product', [])
        instance = instance if instance else Order.objects.create(
            **validated_data)
        quantities = []

        for product_data in products_data:
            product = product_data.pop('product')
            quantities.append(
                Quantity(order=instance, product=product, **product_data))

        return instance, quantities

    def _update_instance(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
