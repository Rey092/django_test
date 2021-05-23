from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Author, Book, Category, Post


# @receiver(pre_save, sender=Post)
# def post_pre_save(sender, instance, *args, **kwargs):
#     instance.full_clean()


@receiver(post_save, sender=Post)
def post_post_save(sender, instance, created, *args, **kwargs):
    cache.delete('posts_list_qs')


@receiver(post_delete, sender=Post)
def post_post_delete(sender, instance, *args, **kwargs):
    cache.delete('posts_list_qs')


@receiver(post_save, sender=Author)
def author_post_save(sender, instance, created, *args, **kwargs):
    cache.delete('authors_list_qs')


@receiver(post_delete, sender=Author)
def author_post_delete(sender, instance, *args, **kwargs):
    cache.delete('authors_list_qs')


@receiver(post_save, sender=Category)
def category_post_save(sender, instance, created, *args, **kwargs):
    cache.delete('categories_list_qs')


@receiver(post_delete, sender=Category)
def category_post_delete(sender, instance, *args, **kwargs):
    cache.delete('categories_list_qs')


@receiver(post_save, sender=Book)
def book_post_save(sender, instance, created, *args, **kwargs):
    cache.delete('categories_list_qs')


@receiver(post_delete, sender=Book)
def book_post_delete(sender, instance, *args, **kwargs):
    cache.delete('categories_list_qs')
