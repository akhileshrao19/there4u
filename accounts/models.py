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

    name = models.CharField(max_length=255, verbose_name='city name')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwrgs):
        self.name = self.name.lower()
        return super(City, self).save(*args, **kwrgs)


class Pin(models.Model):
    '''
    Pin model hold the records of pin codes and user model connected to it via foreign key.
    '''
    code = models.CharField(verbose_name='city pin code', max_length=6)

    def full_clean(self, exclude=None, validate_unique=True):
        super(Pin, self).full_clean(exclude, validate_unique)
        if not re.match(r'^[0-9]{6}$', self.code):
            raise ValidationError(
                'Pin code should be 6 digit long')

    def __unicode__(self):
        return self.code


class State(models.Model):
    '''
    State model hold the records of state name and user model connected to it via foreign key.
    '''
    name = models.CharField(max_length=255, blank=False,
                            null=False, verbose_name='state name')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwrgs):
        self.name = self.name.lower()
        return super(State, self).save(*args, **kwrgs)


class User (AbstractUser):
    '''
    User model is extention of AbstractUser provideing basic details of for user.
    It holds following fileds:-
    id:- unique id assigned to every account created
    password :- password use for login to system
    last_login :- last time user login with its credentials
    is_superuser :- Designates that this user has all permissions without explicitly assigning them.
    first_name :- first name.
    last_name :- last name.
    is_staff :- Designates whether the user can log into this admin site
    is_active :- Designates whether this user should be treated as active. Unselect this instead of deleting accounts.
    date_joined :- date the user created  its account
    email :- unique email field, treated as username,
    balance :- balance in user account.
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

    @property
    def name(self):
        return '{} {}'.format(self.first_name, self.last_name)
