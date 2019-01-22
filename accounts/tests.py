# pylint: disable= E1101
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from base64 import b64encode

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory
from rest_framework.authtoken.models import Token

from .models import User, City, State, Pin
from accounts.views import UserView


class UserSetup(APITestCase):
    def setUp(self):
        self.url = reverse('users:user-list')
        self.person_data_obj = {'first_name': 'test',
                                'last_name': 'user',
                                'city':  City.objects.get_or_create(name='abc')[0],
                                'state': State.objects.get_or_create(name='xyz')[0],
                                'pin': Pin.objects.get_or_create(code='123123')[0],
                                }

        self.person_data = {
            'first_name': 'test',
            'last_name': 'user',
            'city': 'abc',
            'state': 'xyz',
            'pin': '123123'
        }

        self._user = {'email': 'asd@gmail.com',
                      'password': 'asdfasdf', }

        self._user.update(self.person_data_obj)
        self.user = User.objects.create_user(**self._user)

        self._user2 = {'email': 'asdfasdf@c.com',
                       'password': 'asdfasdf'}
        self._user2.update(self.person_data_obj)

        self.user2 = User.objects.create_user(**self._user2)


class CreateUser(UserSetup):
    '''
    Test the Create User operation of Api.
    Insuffient data,  duplicate data and successful user creation is tested.
    '''

    def test_create_user(self):
        data = {'email': 'asdd@gmail.com',
                'password': 'asdfasdf',
                }
        data.update(self.person_data)

        response = self.client.post(self.url, data, format='json')

        _id = User.objects.get(email=data['email']).id
        expected_data = {
            'id': b64encode(str(_id)),
            'url': 'http://testserver/api/users/{}/'.format(_id),
            'email': 'asdd@gmail.com',
            'first_name': self.person_data['first_name'],
            'last_name': self.person_data['last_name'],
            'balance': 1000,
            'city': self.person_data['city'],
            'pin': self.person_data['pin'],
            'state': self.person_data['state'],
            'restaurant': [],
            'token': response.data['token']
        }

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content), expected_data)

    def test_create_user_dup(self):

        data = {'email': 'asd@gmail.com',
                'password': 'asdfasdf',
                }
        data.update(self.person_data)
        response = self.client.post(self.url, data, format='json')
        expected_data = {
            "email": [
                "user with this email already exists."
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), expected_data)

    def test_create_user_insufficient_fields(self):
        data = {'email': 'assdd@gmail.com',
                'password': 'asdfasdf',
                }
        data.update(self.person_data)
        data.pop('first_name')
        response = self.client.post(self.url, data, format='json')
        expected_data = {
            "first_name": [
                "This field is required."
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), expected_data)


class RetreiveUser(UserSetup):
    '''
    Test the Retreive User operation of Api.
    unauthorised user,  forbidden user and successful user retreival is tested.
    '''

    def test_retreive_user_unauthorised(self):

        _id = User.objects.get(email=self.user.email).id
        url = reverse('users:user-detail', kwargs={'pk': _id})

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retreive_user_forbidden(self):
        new_user = {'email': 'asasd@gmail.com',
                    'password': 'asdfasdf', }
        new_user.update(self.person_data_obj)
        new_user = User.objects.create_user(**new_user)

        _id = User.objects.get(email=new_user.email).id
        url = reverse('users:user-detail', kwargs={'pk': _id})

        self.client.force_authenticate(user=self.user)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retreive_user(self):
        _id = User.objects.get(email=self.user.email).id

        self.client.force_login(user=self.user)

        url = reverse('users:user-detail', kwargs={'pk': _id})
        response = self.client.get(url, format='json')

        expected_data = {
            'id': b64encode(str(_id)),
            'url': 'http://testserver/api/users/{}/'.format(_id),
            'email': 'asd@gmail.com',
            'first_name': self.person_data['first_name'],
            'last_name': self.person_data['last_name'],
            'balance': 1000,
            'city': self.person_data['city'],
            'pin': self.person_data['pin'],
            'state': self.person_data['state'],
            'restaurant': [],
            'token': response.data['token']
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), expected_data)


class UpdateUser(UserSetup):
    '''
    Test the Update User operation of Api.
    unauthorised user, put and patch, authorised user put and patch is tested.
    '''

    def test_update_user_patch_unauth(self):

        _id = User.objects.get(email=self.user.email).id
        url = reverse('users:user-detail', kwargs={'pk': _id})

        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_put_unauth(self):

        _id = User.objects.get(email=self.user.email).id
        url = reverse('users:user-detail', kwargs={'pk': _id})

        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_patch(self):
        _id = User.objects.get(email=self.user.email).id

        self.client.force_login(user=self.user)

        url = reverse('users:user-detail', kwargs={'pk': _id})
        response = self.client.patch(
            url, {'first_name': 'jaideep'}, format='json')

        expected_data = {
            'id': b64encode(str(_id)),
            'url': 'http://testserver/api/users/{}/'.format(_id),
            'email': 'asd@gmail.com',
            'first_name': 'jaideep',
            'last_name': self.person_data['last_name'],
            'balance': 1000,
            'city': self.person_data['city'],
            'pin': self.person_data['pin'],
            'state': self.person_data['state'],
            'restaurant': [],
            'token': response.data['token']
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), expected_data)

    def test_update_user_put(self):
        _id = User.objects.get(email=self.user.email).id

        self.client.force_login(user=self.user)

        url = reverse('users:user-detail', kwargs={'pk': _id})

        data = {
            'email': 'asd@gmail.com',
            'password': 'asdfasdfasdf',
            'first_name': 'jaideep',
            'last_name': 'asdf',
            'balance': 1000,
            'city': self.person_data['city'],
            'pin': self.person_data['pin'],
            'state': self.person_data['state']
        }

        response = self.client.put(url, data, format='json')

        expected_data = {
            'id': b64encode(str(_id)),
            'url': 'http://testserver/api/users/{}/'.format(_id),
            'email': 'asd@gmail.com',
            'first_name': 'jaideep',
            'last_name': 'asdf',
            'balance': 1000,
            'city': self.person_data['city'],
            'pin': self.person_data['pin'],
            'state': self.person_data['state'],
            'restaurant': [],
            'token': response.data['token']
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), expected_data)


class DeleteUser(UserSetup):
    '''
    Test the Delete User operation of Api.
    unauthorised user,and authorised user delete is tested.
    '''

    def test_delete_user_unauth(self):

        _id = User.objects.get(email=self.user.email).id
        url = reverse('users:user-detail', kwargs={'pk': _id})

        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user(self):
        _id = User.objects.get(email=self.user.email).id

        self.client.force_login(user=self.user)

        url = reverse('users:user-detail', kwargs={'pk': _id})
        response = self.client.delete(url, format='json')

        expected_data = None

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, expected_data)


class AuthUser(UserSetup):

    def setUp(self):
        super(AuthUser, self).setUp()
        self.url = reverse('users:api-auth')

    def test_login(self):

        response = self.client.post(self.url, {
                                    'username': self._user['email'], 'password': self._user['password']}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], self.user.token)

    def test_logout(self):
        self.client.force_authenticate(user=self.user)
        self.user.token

        response = self.client.delete(self.url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Token.objects.filter(user=self.user)), 0)
