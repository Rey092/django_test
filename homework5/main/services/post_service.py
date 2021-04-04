from main.models import Post


def posts_all():
    return Post.objects.all()
