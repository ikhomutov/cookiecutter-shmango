from django.http.response import HttpResponse
from django.urls import path

app_name = 'api'

urlpatterns = [
    path('', lambda request: HttpResponse('OK', content_type='text/plain')),
]
