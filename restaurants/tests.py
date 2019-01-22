# -*- coding: utf-8 -*-
# pylint:disable=E1101
from __future__ import unicode_literals

from django.test import TestCase
from accounts.tests import UserSetup
from .models import Restaurant, RestaurantOwnerMap, Dish, Menu


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
