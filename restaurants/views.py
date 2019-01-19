# pylint:disable=E1101
# -*- coding: utf-8 -*-

from __future__ import unicode_literals


from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny

from .models import Restaurant, Dish
from .serializers import RestaurantSerializer, DishSerializer
# Create your views here.
class RestaurantView(ModelViewSet):

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create' or self.action == 'delete' or self.action == 'update':
            permission_classes = [ IsAdminUser ]
        else :
            permission_classes = [ AllowAny ]
        return [permission() for permission in permission_classes]

class DishView(ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer