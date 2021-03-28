from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about, name='about'),
    path('posts/', views.posts, name='posts'),
    path('posts/create', views.post_create, name='post_create'),
    path('posts/api', views.post_api, name='post_api'),
]
