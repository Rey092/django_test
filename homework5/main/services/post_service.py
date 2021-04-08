from main.models import Post


def posts_all():
    return Post.objects.all()


def posts_by_author(author_id):
    return Post.objects.filter(author_id=author_id)


def post_find(post_id):
    return Post.objects.filter(id=post_id)
