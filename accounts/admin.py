# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import User, City, State, Pin


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'city', 'state', 'pin']


class CityAdmin(admin.ModelAdmin):
    list_display = ['name']


class StateAdmin(admin.ModelAdmin):
    list_display = ['name']


class PinAdmin(admin.ModelAdmin):
    list_display = ['code']


admin.site.register(User, UserAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Pin, PinAdmin)
