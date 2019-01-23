# -*- coding: utf-8 -*-
# pylint:disable=E1101
from __future__ import unicode_literals
import json

from django.test import TestCase

from rest_framework.reverse import reverse
from rest_framework import status

from accounts.tests import UserSetup
from .models import Restaurant, RestaurantOwnerMap, Dish, Menu


def write_file(data):
    with open('dump.json', 'w') as outfile:
        data = json.loads(data)
        outfile.write(json.dumps(data))
    return True


class RestaurantSetup(UserSetup):
    def setUp(self):
        super(RestaurantSetup, self).setUp()
        self.restaurant = Restaurant.objects.create(name="test_restaurant")
        RestaurantOwnerMap.objects.create(
            restaurant=self.restaurant, owner=self.user)
        dishes = [Dish.objects.create(name=dish) for dish in (
            'test_dish1', 'test_dish2', 'test_dish3')]
        self.menu = [Menu.objects.create(restaurant=self.restaurant, dish=dish, rate=rate, quantity=quantity)
                     for dish, rate, quantity in zip(dishes, (30, 40, 50), (5, 7, 9))]


class ListRestaurants(RestaurantSetup):
    def setUp(self):
        super(ListRestaurants, self).setUp()

    def test_list_restaurants(self):
        url = reverse('restaurants:restaurant-list')
        res = self.client.get(url)
        write_file(res.content)
        restaurants = Restaurant.objects.all()
        expected_data = [
            {
                'url': 'http://testserver/api/restaurant/{}/'.format(restaurant.id),
                'menu': [
                    {
                        'dish': menu_item.dish.name,
                        'rate': menu_item.rate,
                        'id': menu_item.id,
                        'quantity': menu_item.quantity
                    }
                    for menu_item in restaurant.menu.all()
                ],
                'id': restaurant.id,
                'name': restaurant.name
            }
            for restaurant in restaurants
        ]
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(res.content), expected_data)


class RetreiveMenu(RestaurantSetup):
    def setUp(self):
        super(RetreiveMenu, self).setUp()

    def test_get_menu_unauth(self):
        url = reverse('restaurants:menu-list')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_menu_admin(self):
        self.user.is_staff = True
        self.user.save()

        self.client.force_authenticate(user=self.user)
        url = reverse('restaurants:menu-list')
        res = self.client.get(url)

        expected_data = [
            {
                'dish': menu_item.dish.name,
                'rate': menu_item.rate,
                'id': menu_item.id,
                'quantity': menu_item.quantity
            } for menu_item in Menu.objects.all()
        ]

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(res.content), expected_data)
    
    