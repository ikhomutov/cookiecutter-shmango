from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('api/', include('{{ cookiecutter.project_slug }}.apps.api.urls', namespace='api')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
