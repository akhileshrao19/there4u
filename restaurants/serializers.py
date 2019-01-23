# pylint:disable=E1101
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueValidator
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.reverse import reverse

from .models import RestaurantOwnerMap, Restaurant, Menu, Dish

User = get_user_model()


class DishSerializer(serializers.RelatedField):
    def to_representation(self, data):
        return data.name

    def to_internal_value(self, data):
        return Dish.objects.get_or_create(name=data.lower())[0]

    class Meta:
        model = Dish
        fields = ['name']


class RestaurantMenu(serializers.ModelSerializer):
    dish = DishSerializer(queryset=Dish.objects.all())
    restaurant = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Restaurant.objects.all())

    class Meta:
        model = Menu
        fields = ('id', 'dish', 'rate', 'restaurant', 'quantity')
        depth = 2
        extra_kwrgs = {
            'id': {
                'read_only': True
            },
            'restaurant': {
                'write_only': True
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
    url = serializers.HyperlinkedIdentityField(
        view_name="restaurants:restaurant-detail",)

    class Meta:
        model = RestaurantOwnerMap
        fields = ('id', 'url', 'restaurant')
        depth = 2


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name')
