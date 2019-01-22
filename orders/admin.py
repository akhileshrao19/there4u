# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Order, OrderDetail

# Register your models here.


class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['order', 'item', 'quantity']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'created_at', 'updated_at']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
