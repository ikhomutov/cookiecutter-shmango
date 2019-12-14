from django.urls import path

from . import views

urlpatterns = [
    path('sign-in/', views.signin_view, name='sign-in'),
    path('sign-out/', views.signout_view, name='sign-out'),
    path(
        'password-change/',
        views.password_change_view,
        name='password-change'
    ),
]
