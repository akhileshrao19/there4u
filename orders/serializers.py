# pylint:disable=E1101
import logging

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueValidator
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.reverse import reverse

from .models import Order, OrderDetail, ACCEPTED
from restaurants.models import Menu
from restaurants.serializers import RestaurantMenu

logger = logging.getLogger(__name__)


class OrderItemSerializer(serializers.ModelSerializer):

    def to_representation(self, data):
        return {
            'item':
            {
                'id': data.item.id,
                'dish': data.item.dish.name,
                'rate': data.item.rate
            },
                'quantity': data.quantity
        }

    class Meta:
        model = OrderDetail
        fields = ('item', 'quantity')
        extra_kwrgs = {
            'item': {
                'read_only': True,
                'help_text': 'order items'
            },
            'quantity': {
                'help': 'order quantity'
            }
        }


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default='0')
    order_detail = OrderItemSerializer(many=True)

    def validate_order_detail(self, order_details):
        # order_details -> Array of details of dictonary {item : <menu model instance> , quantity : int}
        if len(order_details) == 0:
            raise serializers.ValidationError(
                {'detail': 'Order cannot be empty'})

        if self.instance is not None:
            qs = OrderDetail.objects.filter(order=self.instance)[0]
            restaurant = qs.item.restaurant

        else:
            restaurant = order_details[0]['item'].restaurant

        self.total_amount = 0
        for detail in order_details:
            if detail['item'].restaurant != restaurant:
                raise serializers.ValidationError({'detail':
                                                   'all items must belong to same restaurant'})
            if detail['item'].quantity < detail['quantity']:
                raise serializers.ValidationError({'detail':
                                                   'Not enough items {}'.format(detail['item'])})
            self.total_amount += detail['quantity'] * detail['item'].rate
        return order_details

    def create_order_detail(self, order_details, instance):
        for order_detail in order_details:
            OrderDetail.objects.create(
                order=instance, item=order_detail['item'], quantity=order_detail['quantity'])
            order_detail['item'].quantity -= order_detail['quantity']
            order_detail['item'].save()

    def create(self, validated_data):

        order_details = validated_data.pop('order_detail')
        request = self.context.get('request', None)

        if request.user == 'Annonymous':
            logger.critical('Annonymous user making order')

        if self.total_amount > request.user.balance:
            raise serializers.ValidationError({'detail':
                                               "You don't have enough money to purchase order"})

        order = Order.objects.create(user=request.user)

        self.create_order_detail(order_details, order)

        request.user.balance -= self.total_amount
        request.user.save()

        logger.info('order created with {}'.format(order))

        return order

    def update(self, instance, validated_data):
        if instance.status > ACCEPTED:
            raise serializers.ValidationError({'detail':
                                               'Order cannot be updated at this stage'})

        request = self.context.get('request', None)

        order_details = validated_data.pop('order_detail')

        previous_orders = OrderDetail.objects.filter(order=instance)

        total_amount = 0
        for previous_order in previous_orders:
            total_amount += previous_order.quantity*previous_order.item.rate
            previous_order.item.quantity += previous_order.quantity
            previous_order.item.save()
            previous_order.delete()

        self.create_order_detail(order_details, instance)

        request.user.balance += total_amount
        request.user.save()

        return instance

    class Meta:
        model = Order
        fields = ('id', 'status', 'user', 'updated_at', 'order_detail')
        extra_kwrgs = {
            'id': {
                'read_only': True,
                'help_text': 'unique order id'
            },
            'status': {
                'read_only': True,
                'help_text': '''order status,
                            0 : 'placed',
                            1: 'accpted',
                            2: 'in progress',
                            3: 'dispatched',
                            4: 'delivered',
                            5: 'cancelled',
                            6: 'rejected'
                            '''
            },
            'updated_at': {
                'read_only': True,
                'help_text': 'last time order updated'
            }
        }
