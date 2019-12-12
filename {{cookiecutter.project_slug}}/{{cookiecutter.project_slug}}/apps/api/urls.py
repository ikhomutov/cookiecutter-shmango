from django.urls import include
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .users import urls as users_urls

app_name = 'api'
schema_view = get_schema_view(
    openapi.Info(
        title='{{ cookiecutter.project_name }} API',
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('users/', include(users_urls)),
    path('', schema_view.with_ui('swagger', cache_timeout=0)),
]
