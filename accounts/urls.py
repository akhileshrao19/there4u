'''
Urls for user app are created here	
'''
from django.conf.urls import url, include

from rest_framework import routers
from rest_framework.authtoken import views
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserView, AuthView

router = routers.DefaultRouter()
router.register(r'users', UserView)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/$', obtain_auth_token, name='api-auth-token' ),
    url(r'^auth/$', AuthView.as_view(), name='api-auth-logout')
]
