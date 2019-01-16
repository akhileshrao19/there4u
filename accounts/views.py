# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals


# from django.contrib.auth import get_user_model

# from rest_framework import generics, views, response
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from rest_framework.decorators import permission_classes as permission_classes_deco

# from .serializer import UserCreateSerializer, UserRUDSerializer

# User = get_user_model()

# ######
# # class UserViewSet(viewsets.ModelViewSet):
# #     queryset = User.objects.all()
# #     serializer_class = UserSerializer
# ######


# class UserCreateView(generics.CreateAPIView):
#     permission_classes = []
#     queryset = User.objects.all()
#     serializer_class = UserCreateSerializer
#     queryset = User.objects.all()


# class UserRudView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated]
#     lookup_field = 'pk'
#     queryset = User.objects.all()
#     serializer_class = UserRUDSerializer
#     queryset = User.objects.all()

#     @permission_classes_deco((IsAdminUser))
#     def delete(self, request, *args, **kwargs):
#         super().delete(request, *args, **kwargs)
