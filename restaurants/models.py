# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class Restaurants(models.Model):
    name = models.CharField(max_length=255, null=False)
    owner = models.ManyToManyField(User, related_name="owners", related_query_name="owners")

    def __str__(self):
        return self.name 



class Dishes(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    
    def __str__(self):
        return self.name 


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurants, null=False, on_delete=models.CASCADE, related_name="menu", related_query_name="menu")
    dish = models.ForeignKey(Dishes, null=False, on_delete=models.PROTECT, related_name="served_in", related_query_name="served_in")
    rate = models.IntegerField(default=0)
    
    def __str__(self):
        return  "{}-#-{}".format(self.restaurant, self.dish)

    class Meta:
        unique_together = ('restaurant', 'dish')


