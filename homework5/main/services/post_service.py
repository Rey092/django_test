from django.shortcuts import get_object_or_404
from main.models import Comment, Post


def get_all_posts():
    return Post.objects.all().select_related('author_id')


def posts_by_author(author_id):
    return Post.objects.filter(author_id=author_id)


def post_get(post_id):
    return get_object_or_404(Post, pk=post_id)


def get_comments_for_post(post_id):
    return Comment.objects.all().filter(post_id=post_id)
