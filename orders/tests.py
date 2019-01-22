# pylint: disable= E1101
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from base64 import b64encode
import urllib2

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory
from rest_framework.authtoken.models import Token

from .models import Order, OrderDetail
from restaurants.tests import RestaurantSetup
from accounts.views import UserView


# Create your tests here.


class OrderSetup(RestaurantSetup):
    def setUp(self):
        super(OrderSetup, self).setUp()
        self.maxDiff = None


class CreateOrder(OrderSetup):
    '''
    Test the Create Order operation of Api.
    '''

    def setUp(self):
        super(CreateOrder, self).setUp()
        self.order = {
            'order_detail': [{'item': menu_item.id, 'quantity': menu_item.quantity-1} for menu_item in self.menu]
        }

    def test_create_order(self):
        url = reverse('orders:order-list')
        self.client.force_authenticate(user=self.user)

        response = self.client.post(url, self.order, format='json')

        expected_data = {
            "status": response.data['status'],
            "order_detail": [
                {"item": {"dish": "test_dish1", "rate": 30,
                          "id": response.data['order_detail'][0]['item']['id']}, "quantity": 4},
                {"item": {"dish": "test_dish2", "rate": 40,
                          "id": response.data['order_detail'][1]['item']['id']}, "quantity": 6},
                {"item": {"dish": "test_dish3", "rate": 50,
                          "id": response.data['order_detail'][2]['item']['id']}, "quantity": 8}
            ],
            "id": response.data['id'],
            "updated_at": response.data['updated_at']
        }

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content),  expected_data)

    def test_create_order_unauth(self):
        url = reverse('orders:order-list')

        response = self.client.post(url, self.order, format='json')

        expected_data = {
            "detail": "Authentication credentials were not provided."}

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json.loads(response.content),  expected_data)

    def test_create_order_exceed_amount(self):
        url = reverse('orders:order-list')
        self.user.balance = 0
        self.user.save()
        self.client.force_authenticate(user=self.user)

        response = self.client.post(url, self.order, format='json')

        expected_data = {
            "detail": "You don't have enough money to purchase order"}
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content),  expected_data)

    def test_create_order_exceed_quantity(self):
        url = reverse('orders:order-list')
        self.user.balance = 0
        self.user.save()
        self.client.force_authenticate(user=self.user)

        self.order['order_detail'][0]['quantity'] += 2

        response = self.client.post(url, self.order, format='json')

        expected_data = {"order_detail": {
            "detail": "Not enough items test_restaurant-#-test_dish1"}}
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content),  expected_data)


class RetreiveOrder(OrderSetup):
    '''
    Test the Retreive order operation of Api.
    '''

    def setUp(self):
        super(RetreiveOrder, self).setUp()
        self.order = Order.objects.create(user=self.user)
        self.order_detail = [OrderDetail.objects.create(
            order=self.order, item=item, quantity=item.quantity) for item in self.menu]

    def test_retreive_order_unauthorised(self):
        url = reverse('orders:order-list')

        response = self.client.get(url, format='json')

        expected_data = {
            "detail": "Authentication credentials were not provided."}

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json.loads(response.content),  expected_data)

    def test_retreive_all_order(self):
        url = reverse('orders:order-list')

        self.client.force_authenticate(user=self.user)

        response = self.client.get(url, format='json')

        expected_data = [
            {
                "status": response.data[0]['status'],
                "order_detail": [
                    {"item": {"dish": "test_dish1", "rate": 30,
                              "id": response.data[0]['order_detail'][0]['item']['id']}, "quantity": 5},
                    {"item": {"dish": "test_dish2", "rate": 40,
                              "id": response.data[0]['order_detail'][1]['item']['id']}, "quantity": 7},
                    {"item": {"dish": "test_dish3", "rate": 50,
                              "id": response.data[0]['order_detail'][2]['item']['id']}, "quantity": 9}
                ],
                "id": response.data[0]['id'],
                "updated_at": response.data[0]['updated_at']
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),  expected_data)

    def test_retreive_order_with_pk(self):
        url = reverse('orders:order-detail', kwargs={'pk': self.order.id})

        self.client.force_authenticate(user=self.user)

        response = self.client.get(url, format='json')

        expected_data = {
            "status": response.data['status'],
            "order_detail": [
                {"item": {"dish": "test_dish1", "rate": 30,
                          "id": response.data['order_detail'][0]['item']['id']}, "quantity": 5},
                {"item": {"dish": "test_dish2", "rate": 40,
                          "id": response.data['order_detail'][1]['item']['id']}, "quantity": 7},
                {"item": {"dish": "test_dish3", "rate": 50,
                          "id": response.data['order_detail'][2]['item']['id']}, "quantity": 9}
            ],
            "id": response.data['id'],
            "updated_at": response.data['updated_at']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),  expected_data)


class UpdateOrder(OrderSetup):
    def setUp(self):
        super(UpdateOrder, self).setUp()
        self.order = Order.objects.create(user=self.user)
        self.order_detail = [OrderDetail.objects.create(
            order=self.order, item=item, quantity=item.quantity) for item in self.menu]

    def test_update_order_unauth(self):
        url = reverse('orders:order-detail', kwargs={'pk': self.order.id})

        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_order_put(self):
        url = reverse('orders:order-detail', kwargs={'pk': self.order.id})
        new_data = {
            'order_detail': [{'item': menu_item.id, 'quantity': menu_item.quantity-1} for menu_item in self.menu]
        }
        new_data['order_detail'].pop(0)

        self.client.force_authenticate(user=self.user)

        response = self.client.put(url, new_data, format='json')
        expected_data = {
            "status": response.data['status'],
            "order_detail": [
                {"item": {"dish": "test_dish2", "rate": 40,
                          "id":  response.data['order_detail'][0]['item']['id']}, "quantity": 6},
                {"item": {"dish": "test_dish3", "rate": 50,
                          "id":  response.data['order_detail'][1]['item']['id']}, "quantity": 8}
            ],
            "id": response.data['id'],
            "updated_at": response.data['updated_at']
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), expected_data)

    def test_update_order_unauth2(self):
        url = reverse('orders:order-detail', kwargs={'pk': self.order.id})
        new_data = {
            'order_detail': [{'item': menu_item.id, 'quantity': menu_item.quantity-1} for menu_item in self.menu]
        }
        new_data['order_detail'].pop(0)

        self.client.force_authenticate(user=self.user2)
        response = self.client.put(url, new_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CancelOrder(OrderSetup):
    def setUp(self):
        super(CancelOrder, self).setUp()
        self.order = Order.objects.create(user=self.user)
        self.order_detail = [OrderDetail.objects.create(
            order=self.order, item=item, quantity=item.quantity) for item in self.menu]

    def test_cancel_unauth(self):
        url = reverse('orders:order-cancel', kwargs={'pk': self.order.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cancel_unauth2(self):
        url = reverse('orders:order-cancel', kwargs={'pk': self.order.id})
        self.client.force_login(user=self.user2)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cancel(self):
        url = reverse('orders:order-cancel', kwargs={'pk': self.order.id})
        self.client.force_login(user=self.user)

        current_balance = self.user.balance
        response = self.client.delete(url, format='json')
        self.user = (get_user_model()).objects.get(pk=self.user.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(current_balance < self.user.balance)


class SearchOrder(OrderSetup):
    def setUp(self):
        super(SearchOrder, self).setUp()
        self.order = Order.objects.create(user=self.user)
        self.order_detail = [OrderDetail.objects.create(
            order=self.order, item=item, quantity=item.quantity) for item in self.menu]

    def test_search_order_unauth(self):
        url = '{}?restaurant={}'.format(
            reverse('orders:order-search'), self.menu[0].restaurant)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_search_order_restaurant(self):
        self.client.force_authenticate(user=self.user)

        url = '{}?restaurant={}'.format(
            reverse('orders:order-search'), self.menu[0].restaurant)
        response = self.client.get(url)

        expected_data = [
            {
                "status": 0,
                "order_detail": [
                    {"item": {"dish": "test_dish1", "rate": 30,
                              "id": response.data[0]['order_detail'][0]['item']['id']}, "quantity": 5},
                    {"item": {"dish": "test_dish2", "rate": 40,
                              "id": response.data[0]['order_detail'][1]['item']['id']}, "quantity": 7},
                    {"item": {"dish": "test_dish3", "rate": 50,
                              "id": response.data[0]['order_detail'][2]['item']['id']}, "quantity": 9}
                ],
                "id": response.data[0]['id'],
                "updated_at": response.data[0]['updated_at']
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), expected_data)

    def test_search_order_item(self):
        self.client.force_authenticate(user=self.user)

        url = '{}?item={}'.format(
            reverse('orders:order-search'), self.menu[0].dish)
        response = self.client.get(url)

        expected_data = [
            {
                "status": 0,
                "order_detail": [
                    {"item": {"dish": "test_dish1", "rate": 30,
                              "id": response.data[0]['order_detail'][0]['item']['id']}, "quantity": 5},
                    {"item": {"dish": "test_dish2", "rate": 40,
                              "id": response.data[0]['order_detail'][1]['item']['id']}, "quantity": 7},
                    {"item": {"dish": "test_dish3", "rate": 50,
                              "id": response.data[0]['order_detail'][2]['item']['id']}, "quantity": 9}
                ],
                "id": response.data[0]['id'],
                "updated_at": response.data[0]['updated_at']
            }
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), expected_data)
