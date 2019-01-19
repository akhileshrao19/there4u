# pylint:disable=E1101
# -*- coding: utf-8 -*-

import base64
import re

from django.contrib.auth import get_user_model

from rest_framework import serializers, exceptions

from accounts.models import Pin, City, State
from restaurants.serializers import RestaurantOwnerSerializer
from restaurants.models import RestaurantOwnerMap

User = get_user_model()


class CitySerializer(serializers.RelatedField):
    '''
    City serializer belong to city model. 
    This particularly use to manuplate the representation of input city and
     provide abstraction to storage of data in database.
    '''

    def to_representation(self, value):
        return value.name

    def to_internal_value(self, data):
        return City.objects.get_or_create(name=data)[0]


class StateSerializer(serializers.RelatedField):
    '''
    State serializer belong to state model. 
    This particularly use to manuplate the representation of input state and
     provide abstraction to storage of data in database.
    '''

    def to_representation(self, value):
        return value.name

    def to_internal_value(self, data):
        return State.objects.get_or_create(name=data)[0]


class PinSerializer(serializers.RelatedField):
    '''
    Pin serializer belong to pin model. 
    This particularly use to manuplate the representation of input pin and
     provide abstraction to storage of data in database.
    '''

    def pinValidator(self, data):
        if re.match(r'^[0-9]{6}$', str(data)) is None:
            raise serializers.ValidationError(
                'Pin must be 6 digit numerical value')
        return True

    def to_representation(self, value):
        return value.code

    def to_internal_value(self, data):
        self.pinValidator(data)
        return Pin.objects.get_or_create(code=data)[0]

    def create(self, validated_data):
        print validated_data
        return Pin.objects.get_or_create(name='asdfas')


class UserSerializer(serializers.ModelSerializer):
    '''
    User serializer belong to User model. 
    This particularly use for the user related CRUD operations.
    It is linked to CitySerializer, StateSerializer, PinSerializer to provide level of abstraction.
    '''
    url = serializers.HyperlinkedIdentityField(
        view_name='users:user-detail', lookup_field='pk', read_only=True)
    city = CitySerializer(many=False, queryset=City.objects.all(), help_text='city of user, required')
    state = StateSerializer(many=False, queryset=State.objects.all(), help_text='state of user, required')
    pin = PinSerializer(queryset=Pin.objects.all(), help_text='pincode of user,  must be six digit numeric value, required' )
    id = serializers.SerializerMethodField(read_only=True)
    restaurant = RestaurantOwnerSerializer(
        many=True, read_only=True, required=False)

    def get_id(self, obj):
        return base64.b64encode(str(obj.id))

    def validate_email(self, value):
        qs = User.objects.filter(email=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError('This email is already taken')
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance = super(UserSerializer, self).update(instance, validated_data)

        if validated_data.get('password', None):
            instance.set_password(validated_data.get('password'))

        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('id', 'url', 'email', 'password', 'first_name',
                  'last_name', 'balance', 'city', 'pin', 'state', 'restaurant')
        extra_kwargs = {
                        'email': {
                            'help_text':'email field, need to be unique, will be trated as username, required'
                        },
                        'password': {   
                                'write_only': True,
                                'help_text': 'password for the account, required'
                        },
                        'first_name' :{
                                'help_text': 'user first_name, required'
                        },
                        'last_name' : {
                            'help_text' : 'user last_name'
                        },
                        'balance' : {
                            'help_text' : 'user balance, default is 0, value must be integer'
                        }
        }
