from main.models import Post


def posts_all():
    return Post.objects.all()


def posts_by_author(author_id):
    data = Post.objects.filter(author_id=author_id)
    return data
