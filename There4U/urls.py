
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='There4U',)

urlpatterns = [
    url(r'^api/', include('accounts.urls', namespace='users') ),
    url(r'^api/', include('restaurants.urls', namespace='restaurants') ),
    url(r'^api/', include('orders.urls', namespace='orders') ),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', schema_view)
]
