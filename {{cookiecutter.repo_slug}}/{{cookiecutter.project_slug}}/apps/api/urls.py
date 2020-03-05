from django.urls import include
from django.urls import path
from rest_framework import permissions

from .users import urls as users_urls

app_name = 'api'

urlpatterns = [
    path('users/', include(users_urls)),
]
