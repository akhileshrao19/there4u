# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser



class City (models.Model):
    name = models.CharField(max_length=255, null=False, verbose_name="city name" )

    def __str__(self):
        return self.name

class Zip(models.Model):
    code = models.IntegerField(verbose_name="city zip code", null=False)

    def __str__(self):
        return self.code

class State(models.Model):
    name = models.CharField(max_length=255, null=False, verbose_name="state name")

    def __str__(self):
        return self.name



class User (AbstractUser):
    city = models.ForeignKey(City, null=True, on_delete=models.PROTECT)
    zip = models.ForeignKey(Zip, null=True, on_delete=models.PROTECT)
    state = models.ForeignKey(State, null=True, on_delete=models.PROTECT)
    balance = models.IntegerField(default=1000, verbose_name="available balance in account")

    @property
    def name(self):
        return '{} {}'.format(self.first_name, self.last_name) 
