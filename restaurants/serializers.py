
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
    class Meta:
        model = Dish
        fields = ['name']



class RestaurantMenu(serializers.ModelSerializer):
    dish = DishSerializer(many=False, read_only=True)

    class Meta:
        model = Menu
        fields = ('id', 'dish', 'rate')
        depth = 2
        extra_kwrgs = {
            'id':{
                'read_only':True
                }
            }


class RestaurantSerializer(serializers.ModelSerializer):
    menu = RestaurantMenu(many=True)
    url = serializers.HyperlinkedIdentityField(
        view_name="restaurant:restaurant-detail", lookup_field='pk')
    

    class Meta:
        model = Restaurant
        fields = ('id', 'url', 'name', 'menu')


class RestaurantOwnerSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name= "restaurant:restaurant-detail",)
    class Meta:
        model = RestaurantOwnerMap
        fields = ('id', 'url','restaurant')
        depth = 2