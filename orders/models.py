# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from restaurants.models import Menu
from django.contrib.auth import get_user_model


# Create your models here.

IN_PROGRESS = "IP"
DISPATCHED = "DP"
DELIVERED = "DL"
CANCELLED = "CL"

ORDER_STATUS = {
    IN_PROGRESS : "in progress",
    DISPATCHED : "dispatched",
    DELIVERED : "delivered",
    CANCELLED : "cancelled"
} 


User = get_user_model()



class Order(models.Model):
    ORDER_STATUS_l = (
        (IN_PROGRESS, "in progress"),
        (DISPATCHED, "dispatched"),
        (DELIVERED, "delivered"), 
        (CANCELLED, "cancelled")
        )
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orders", related_query_name="orders")
    date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=ORDER_STATUS_l, max_length=2, default= IN_PROGRESS)
    items = models.ManyToManyField(Menu, related_name="in_orders", related_query_name="in_orders")
    
    def __str__(self):
        return "{}-#-{}-#-{}".format(self.user, self.date, ORDER_STATUS[self.status])
    