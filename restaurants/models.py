# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name


class RestaurantOwnerMap(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, related_name='owner', on_delete=models.PROTECT)
    owner = models.ForeignKey(User, related_name='restaurant',
                              on_delete=models.PROTECT)

    def __unicode__(self):
        return '{}-#-{}'.format(self.restaurant, self.owner.name)

    class Meta:
        unique_together = ('restaurant', 'owner')


class Dish(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Dishes'


class Menu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,  on_delete=models.CASCADE, related_name='menu')
    dish = models.ForeignKey(
        Dish, on_delete=models.PROTECT, related_name='served_in')
    rate = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(
        default=10, verbose_name="available quantity")

    def __unicode__(self):
        return '{}-#-{}'.format(self.restaurant, self.dish)

    class Meta:
        unique_together = ('restaurant', 'dish')
