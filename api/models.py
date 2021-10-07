from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, FloatField, TextField

from bulk_update_or_create import BulkUpdateOrCreateQuerySet

User = get_user_model()


class Product(models.Model):
    name = CharField('Name', max_length=250)
    price = FloatField('Price')
    description = TextField('Description', null=True, blank=True)

    class Meta:
        ordering = ['name', 'price']


class Order(models.Model):
    tracking_number = CharField(
        'Tracking number', max_length=15, editable=False)
    address = CharField(max_length=250)
    shipping_costs = FloatField('Shipping costs', default=0.00, editable=False)
    total_price = FloatField('Total price', default=0.00, editable=False)

    user = models.ForeignKey(User, related_name='orders',
                             editable=False, on_delete=CASCADE)
    products = models.ManyToManyField(
        Product, through='Quantity', related_name='orders')

    class Meta:
        ordering = ['tracking_number', 'shipping_costs']


class Quantity(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    order = models.ForeignKey(
        Order, related_name='order_to_product', on_delete=CASCADE)
    product = models.ForeignKey(
        Product, related_name='product_to_order', on_delete=CASCADE)
    quantity = models.PositiveSmallIntegerField('Quantity')
