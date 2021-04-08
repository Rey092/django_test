"""Настройки маршрутизатора."""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about, name='about'),
    path('posts/', views.posts, name='posts_all'),
    path('posts/<int:author_id>', views.author_posts, name='posts_by_author'),
    path('post/create', views.post_create, name='post_create'),
    path('post/show/<int:post_id>', views.post_show, name='post_show'),
    path('posts/update/<int:post_id>', views.post_update, name='post_update'),
    path('subscribers/new', views.subscribers_new, name='subscribers_new'),
    path('subscribers/all', views.subscribers_all, name='subscribers_all'),
    path('authors/new', views.authors_new, name='authors_new'),
    path('authors/all', views.authors_all, name='authors_all'),

    path('api/posts', views.api_posts, name='api_posts'),
    path('api/subscribe', views.api_subscribe, name='api_subscribe'),
    path('api/authors/new', views.api_authors_new, name='api_authors_new'),
]
