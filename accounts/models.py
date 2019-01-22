# pylint:disable=E1101
# -*- coding: utf-8 -*-
'''
Models belonging to user are defined here
Pin model store Pincode
State model store State name
City model store State name
User model is extention of AbstractBase user to remove username from AbstractUser.
'''

from __future__ import unicode_literals

import re

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as ParentUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token


class UserManager(ParentUserManager):
    '''
    UserManger is the extension of inbuilt UserManager of Abstract User.
    It is created to completely remove username from database and handle
    creation of user operation without username. Email is treated as unique username field.
    '''

    def _create_user(self, email, password, **extra_fields):
        '''
        Creates and saves a User with the given email and password.
        '''

        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        # username = self.model.normalize_username(username)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class City (models.Model):
    '''
    City model hold the records of city and user model connected to it via foreign key.
    '''

    name = models.CharField(
        max_length=255, verbose_name='city name', unique=True)

    def __unicode__(self):
        return self.name
    
    def clean_name(self):
        return self.cleaned_data['name'].lower()

class Pin(models.Model):
    '''
    Pin model hold the records of pin codes and user model connected to it via foreign key.
    '''
    code = models.CharField(verbose_name='city pin code',
                            max_length=6, unique=True)

    def clean_code(self ):
        if not re.match(r'^[0-9]{6}$', self.cleaned_data['code']):
            raise ValidationError({'detail':
                'Pin code should be 6 digit long'})
        return self.cleaned_data['code']

    def __unicode__(self):
        return self.code


class State(models.Model):
    '''
    State model hold the records of state name and user model connected to it via foreign key.
    '''
    name = models.CharField(max_length=255, blank=False,
                            null=False, verbose_name='state name', unique=True)

    def __unicode__(self):
        return self.name

    def clean_name(self):
        return self.cleaned_data['name'].lower()

class User (AbstractUser):
    '''
    User model is extention of AbstractUser provideing basic details of for user.
    '''
    username = None
    first_name = models.CharField(
        blank=False, max_length=30, verbose_name='first name')
    email = models.EmailField(blank=False, unique=True)
    city = models.ForeignKey(City, null=False, on_delete=models.PROTECT)
    pin = models.ForeignKey(Pin, null=False, on_delete=models.PROTECT)
    state = models.ForeignKey(State, null=False, on_delete=models.PROTECT)
    balance = models.IntegerField(
        default=1000, verbose_name='available balance in account')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def clean_email(self):
        return self.cleaned_data['email'].lower()

    @property
    def name(self):
        return '{} {}'.format(self.first_name, self.last_name)
    @property
    def token(self):
        return Token.objects.get_or_create(user=self)[0].key
