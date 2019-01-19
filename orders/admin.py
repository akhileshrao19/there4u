# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Order, OrderDetail

# Register your models here.


class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['order', 'item', 'quantity']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'created_date', 'updated_date']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
