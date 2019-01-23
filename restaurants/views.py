# pylint:disable=E1101
# -*- coding: utf-8 -*-

from __future__ import unicode_literals


from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAdminUser, AllowAny, BasePermission, IsAuthenticated
from rest_framework.decorators import action
from rest_framework import response, status
from rest_framework.exceptions import PermissionDenied

from .models import Restaurant, Dish, Menu
from .serializers import RestaurantSerializer, DishSerializer, RestaurantMenu, CustomerSerializer

User = get_user_model


class IsAdminOrOwner(BasePermission):
    def has_object_permission(self, request, view, menuItem):
        return request.user.is_staff or len(request.user.restaurant.filter(pk=menuItem.restaurant.id)) > 0


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

    @action(detail=True, methods=['get'])
    def customers(self, request, pk):
        try:
            restaurant = Restaurant.objects.get(pk=pk)
            if len(restaurant.owner.filter(owner=request.user)) > 0 or request.user.is_staff:
                users = User.objects.filter(
                    orders__order_detail__item__restaurant=restaurant).distinct()
                serializer = CustomerSerializer(users, many=True)
                return response.Response(serializer.data, status=status.HTTP_200_OK)
            raise PermissionDenied(
                {'detail': 'you are not the owner of this restaurant'})
        except Restaurant.DoesNotExist:
            return response.Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        '''
        Instantiates and returns the list of permissions that this view requires.
        '''
        if self.action == 'create' or self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAdminUser]
        elif self.action == 'customer':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class MenuView(ModelViewSet):
    serializer_class = RestaurantMenu
    queryset = Menu.objects.all()

    def get_permissions(self):
        '''
        Instantiates and returns the list of permissions that this view requires.
        '''
        if self.action == 'retrieve' or self.action == 'create' or self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated, IsAdminOrOwner]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
