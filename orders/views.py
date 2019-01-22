# pylint:disable=E1101
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from django.shortcuts import render

from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAdminUser, AllowAny, BasePermission, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, mixins
from rest_framework.exceptions import NotFound, PermissionDenied

from .serializers import OrderSerializer
from .models import Order, CANCELLED, OrderDetail, IN_PROGRESS
from restaurants.models import Restaurant, Menu

logger = logging.getLogger(__name__)


class IsAdminOrSelf(BasePermission):
    """
    Object-level permission to only allow modifications to a User object
    if the request.user is an administrator or you are modifying your own
    user object.
    """

    def has_object_permission(self, request, view, obj):
        print
        return request.user.is_staff or request.user == obj.user


class OrderView(mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.ListModelMixin,
                GenericViewSet):
    '''
    retrieve:
        Return order details,  authentication required.

    create:
        Create new order

    update:
        Update order details, only if order is under inprogress stage, authentication required

    partial_update:
        Update partial of order detail, only if order is under inprogress stage, authentication required

    list:
        list orders , authentication required, admin can list all order

    cancel:
        Change status of order to cancel, only if order is under inprogress stage, authentication required, admin can change at any stage

    search:
        filter orders on the basis of restaurant or item or both
    '''
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def serach_query(self, request, restaurant=None, item=None):
        query_set = None
        if restaurant:
            if request.user.is_staff:
                query_set = self.queryset.filter(
                    order_detail__item__restaurant__name__icontains=restaurant)
            else:
                query_set = self.queryset.filter(
                    user=request.user, order_detail__item__restaurant__name__icontains=restaurant)
        if item:
            if request.user.is_staff:
                qs1 = self.queryset.filter(
                    order_detail__item__dish__name__icontains=item)
            else:
                qs1 = self.queryset.filter(
                    user=request.user, order_detail__item__dish__name__icontains=item)
            if query_set is not None:
                query_set.union(qs1)
            else:
                query_set = qs1

        return query_set.distinct()

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            self.queryset = request.user.orders
        return super(OrderView, self).list(request,  *args, **kwargs)

    @action(detail=True, methods=['delete'])
    def cancel(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            if not request.user.is_staff and order.user != request.user:
                return Response({'detail': "order not belong touser"}, status=status.HTTP_403_FORBIDDEN)
            elif order.status >= IN_PROGRESS:
                raise PermissionDenied(detail="order already in progress")
        except Order.DoesNotExist:
            raise NotFound(detail="order not exist")

        order.status = CANCELLED
        order.save()
        order_details = OrderDetail.objects.filter(order=order)

        revert_amount = 0
        for order_detail in order_details:
            order_detail.item.quantity += order_detail.quantity
            revert_amount += order_detail.item.rate*order_detail.quantity

        request.user.balance += revert_amount
        request.user.save()

        logger.info('order {} cancelled'.format(order))
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def search(self, request):
        restaurant = request.GET.get('restaurant', None)
        item = request.GET.get('item', None)

        item = item.lower() if item is not None else None
        restaurant = restaurant.lower() if restaurant is not None else None

        query_set = self.serach_query(request, restaurant, item)

        serializer = self.serializer_class(query_set, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create' or self.action == 'list' or self.action == 'cancel' or self.action == 'search':
            permission_classes = [IsAuthenticated]
        elif self.action == 'update' or self.action == 'partial_update' or self.action == 'retrieve':
            permission_classes = [IsAdminOrSelf]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
