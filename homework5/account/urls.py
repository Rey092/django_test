"""Настройки маршрутизатора."""
from django.urls import path

from . import views

urlpatterns = [
    path('my-profile/', views.MyProfileUpdateView.as_view(), name='my_profile'),
    path('login/', views.LoginView.as_view(success_url='/'), name='login'),
]
