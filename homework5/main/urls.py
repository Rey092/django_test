"""Настройки маршрутизатора."""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about, name='about'),
    path('posts/', views.posts, name='posts'),
    path('posts/create', views.post_create, name='post_create'),
    path('posts/subscribe', views.posts_subscribe, name='posts_subscribe'),

    path('api/posts', views.api_posts, name='api_posts'),
    path('api/subscribe', views.api_subscribe, name='api_subscribe'),
]
