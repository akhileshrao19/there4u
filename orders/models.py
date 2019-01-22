# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model

from restaurants.models import Menu

# Create your models here.
PLACED = 0
ACCEPTED = 1
IN_PROGRESS = 2
DISPATCHED = 3
DELIVERED = 4
CANCELLED = 5
REJECTED = 6

ORDER_STATUS = {
    PLACED : 'placed',
    ACCEPTED: 'accpted',
    IN_PROGRESS: 'in progress',
    DISPATCHED: 'dispatched',
    DELIVERED: 'delivered',
    CANCELLED: 'cancelled',
    REJECTED: 'rejected'
}


User = get_user_model()


class Order(models.Model):
    ORDER_STATUS_l = (
        (PLACED, 'placed'),
        (IN_PROGRESS, 'in progress'),
        (ACCEPTED, 'accepted'),
        (DISPATCHED, 'dispatched'),
        (DELIVERED, 'delivered'),
        (CANCELLED, 'cancelled'),
        (REJECTED, 'rejected')
    )
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(
        choices=ORDER_STATUS_l, default=PLACED)
    # items = models.ManyToManyField(Menu, related_name='in_orders', related_query_name='in_orders')

    def __unicode__(self):
        return '{}-#-{}-#-{}-#-{}'.format(self.pk, self.user, self.created_at, ORDER_STATUS[self.status])


class OrderDetail(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT, related_name='order_detail')

    item = models.ForeignKey(
        Menu, on_delete=models.SET_NULL, related_name='in_order', null=True)

    quantity = models.PositiveIntegerField(
        default=0, verbose_name='order quantity')

    def __unicode__(self):
        return '{}-#-{}'.format(self.order, self.item)

    class Meta:
        unique_together = ('item', 'order')
