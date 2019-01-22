#pylint:disable=E1101
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueValidator
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.reverse import reverse

from .models import RestaurantOwnerMap, Restaurant, Menu, Dish


class DishSerializer(serializers.ModelSerializer):
    def to_representation(self, data):
        return data.name
    
    def to_internal_value(self, data):
        print data
        return Dish.objects.get_or_create(name=data.lower())
    class Meta:
        model = Dish
        fields = ['name']



class RestaurantMenu(serializers.ModelSerializer):
    dish = DishSerializer( read_only=True)

    class Meta:
        model = Menu
        fields = ('id', 'dish', 'rate', 'restaurant')
        depth = 2
        extra_kwrgs = {
            'id':{
                'read_only':True
                },
            'restaurant':{
                'write_only':True
                }
            }


class RestaurantSerializer(serializers.ModelSerializer):
    menu = RestaurantMenu(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name="restaurants:restaurant-detail", lookup_field='pk')
    

    class Meta:
        model = Restaurant
        fields = ('id', 'url', 'name', 'menu')



class RestaurantOwnerSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name= "restaurants:restaurant-detail",)
    class Meta:
        model = RestaurantOwnerMap
        fields = ('id', 'url','restaurant')
        depth = 2