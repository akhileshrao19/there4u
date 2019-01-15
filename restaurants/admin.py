# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Restaurants, Menu, Dishes

# Register your models here.

class RestaurantsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class MenuAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'dish', 'rate']
    

class DishesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    

admin.site.register(Restaurants, RestaurantsAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Dishes, DishesAdmin)