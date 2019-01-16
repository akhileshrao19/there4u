# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Restaurant, Menu, Dish, RestaurantOwnerMap


# Register your models here.


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class RestaurantOwnerMapAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'owner']


class MenuAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'dish', 'rate']


class DishAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(RestaurantOwnerMap, RestaurantOwnerMapAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Dish, DishAdmin)
