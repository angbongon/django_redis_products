import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DecimalField, TextField, UUIDField

from bulk_update_or_create import BulkUpdateOrCreateQuerySet

User = get_user_model()


class Product(models.Model):
    name = CharField('Name', max_length=250)
    price = DecimalField('Price', max_digits=10, decimal_places=2)
    description = TextField('Description', null=True, blank=True)

    class Meta:
        ordering = ['name', 'price']


class Order(models.Model):
    tracking_number = UUIDField(
        'Tracking number', default=uuid.uuid4, editable=False)
    address = CharField(max_length=250)
    shipping_costs = DecimalField(
        'Shipping costs', max_digits=10, decimal_places=2, default=0.00)

    user = models.ForeignKey(User, related_name='orders',
                             editable=False, on_delete=CASCADE)
    products = models.ManyToManyField(
        Product, through='Quantity', related_name='orders', blank=True)

    class Meta:
        ordering = ['tracking_number', 'shipping_costs']


class Quantity(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    order = models.ForeignKey(
        Order, related_name='order_to_product', on_delete=CASCADE)
    product = models.ForeignKey(
        Product, related_name='product_to_order', on_delete=CASCADE)
    quantity = models.PositiveSmallIntegerField('Quantity')
