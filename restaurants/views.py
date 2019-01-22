# pylint:disable=E1101
# -*- coding: utf-8 -*-

from __future__ import unicode_literals


from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAdminUser, AllowAny

from .models import Restaurant, Dish
from .serializers import RestaurantSerializer, DishSerializer
# Create your views here.


class RestaurantView(ModelViewSet):
    '''
    retrieve:
        Return restaurant details

    create:
        Create restaurant User, admin permission required

    destroy:
        Delete restaurant from the db, admin permission required

    update:
        Update restaurant details in db, admin permission required

    partial_update:
        Update partial of restaurant detail, admin permission required

    list:
        List all restaurants with therir details
    '''
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_permissions(self):
        '''
        Instantiates and returns the list of permissions that this view requires.
        '''
        if self.action == 'create' or self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAdminUser]
        # elif self.action == 'update' or self.action == 'partial_update':
        #     permission_classes = [IsAdminOrOwner]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
