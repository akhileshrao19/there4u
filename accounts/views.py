# pylint:disable=E1101
# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, response, status
from rest_framework.permissions import IsAdminUser, BasePermission
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


from .serializers import UserSerializer
User = get_user_model()


class IsAdminOrSelf(BasePermission):
    """
    Object-level permission to only allow modifications to a User object
    if the request.user is an administrator or you are modifying your own
    user object.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user == obj


class UserView(mixins.CreateModelMixin,
               mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               GenericViewSet):
    """
    retrieve:
        Return user details

    create:
        Create new User

    destroy:
        Delete user from the db

    update:
        Update user details in db

    partial_update:
        Update partial of user detail
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = []
        elif self.action == 'list':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAdminOrSelf]
        return [permission() for permission in permission_classes]


class AuthView(APIView):
    '''
    Auth View handle auth related operations logout (remove auth token from the db).
    '''
    def delete(self, request, *args, **kwrds):
        if request.user.is_authenticated:
            Token.objects.get(user=request.user).delete()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        return response.Response(status=status.HTTP_401_UNAUTHORIZED)
