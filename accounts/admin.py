# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import User, City, State, Pin


class UserAdmin(admin.ModelAdmin):
    '''
    UserAdmin to be use with django admin app.
    '''
    list_display = ['email', 'id', 'first_name',
                    'last_name', 'city', 'state', 'pin', 'balance']


class CityAdmin(admin.ModelAdmin):
    '''
    CityAdmin to be use with django admin app.
    '''
    list_display = ['name']


class StateAdmin(admin.ModelAdmin):
    '''
    StateAdmin to be use with django admin app.
    '''
    list_display = ['name']


class PinAdmin(admin.ModelAdmin):
    '''
    PinAdmin to be use with django admin app.
    '''
    list_display = ['code']


admin.site.register(User, UserAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Pin, PinAdmin)
