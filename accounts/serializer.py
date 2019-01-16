# from rest_framework import serializers, exceptions
# from django.contrib.auth import authenticate
# from django.contrib.auth import get_user_model


# User = get_user_model()


# class UserCreateSerializer(serializers.ModelSerializer):

#     def create(self, validated_data):
#         print validated_data
#         instance = self.Meta.model.objects.create_user(
#             username=validated_data.get('username'),
#             password=validated_data.get('password'),
#             first_name=validated_data.get('first_name'),
#             last_name=validated_data.get('last_name'),
#             city=validated_data.get('city'),
#             zip=validated_data.get('zip'),
#             state=validated_data.get('state')
#         )

#         return instance

#     class Meta:
#         model = User
#         fields = ('username', 'password', 'first_name',
#                   'last_name', 'email', 'city', 'zip', 'state')


# class UserRUDSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name',
#                   'email', 'city', 'zip', 'state')
