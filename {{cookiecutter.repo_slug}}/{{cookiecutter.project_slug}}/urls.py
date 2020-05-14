from django.conf import settings
from django.contrib import admin
{%- if cookiecutter.use_rest_framework == 'y' %}
from django.urls import include
from django.urls import path
{%- endif %}

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    {%- if cookiecutter.use_rest_framework == 'y' %}
    path('api/', include('{{ cookiecutter.project_slug }}.apps.api.urls', namespace='api')),
    {%- endif %}
]
