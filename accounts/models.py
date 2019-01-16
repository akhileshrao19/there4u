# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as ParentUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.core.exceptions import ValidationError
import re


class City (models.Model):
    name = models.CharField(max_length=255, verbose_name='city name')

    def __unicode__(self):
        return self.name


class Pin(models.Model):
    code = models.CharField(verbose_name='city pin code', max_length=6)

    def full_clean(self, exclude=None, validate_unique=True):
        super(Pin, self).full_clean(exclude, validate_unique)
        if not re.match(r'^[0-9]{6}$', self.code):
            raise ValidationError(
                'Pin code should be 6 digit long')

    def __unicode__(self):
        return self.code


class State(models.Model):
    name = models.CharField(max_length=255, blank=False,
                            null=False, verbose_name='state name')

    def __unicode__(self):
        return self.name


class UserManager(ParentUserManager):

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


class User (AbstractUser):
    username = None
    email = models.EmailField(blank=False, unique=True)
    city = models.ForeignKey(City, null=True, on_delete=models.PROTECT)
    pin = models.ForeignKey(Pin, null=True, on_delete=models.PROTECT)
    state = models.ForeignKey(State, null=True, on_delete=models.PROTECT)
    balance = models.IntegerField(
        default=1000, verbose_name='available balance in account')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def name(self):
        return '{} {}'.format(self.first_name, self.last_name)

# class User (AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField( null=False, unique=True, help_text=Required. email is going to use as username)
#     first_name = models.CharField( max_length=30, blank=True)
#     last_name = models.CharField( max_length=30, blank=True)
#     is_active = models.BooleanField( default=True,help_text='''Designates whether this user should be treated as active. Unselect this instead of deleting accounts.''',)
#     is_staff = models.BooleanField( default=False, help_text='Designates whether the user can log into this admin site.',)

#     city = models.ForeignKey(City, null=True, on_delete=models.PROTECT)
#     zip = models.ForeignKey(Zip, null=True, on_delete=models.PROTECT)
#     state = models.ForeignKey(State, null=True, on_delete=models.PROTECT)
#     balance = models.IntegerField(default=1000, verbose_name=available balance in account)


#     USERNAME_FIELD = 'email'
#     EMAIL_FIELD = 'email'

#     @property
#     def full_name(self):
#
#         Returns the first_name plus the last_name, with a space in between.
#
#         full_name = '%s %s' % (self.first_name, self.last_name)
#         return full_name.strip()

#     # def clean(self):
#     #     super(AbstractUser, self).clean()
#     #     self.email = self.__class__.objects.normalize_email(self.email)
