from main.models import Author


def authors_all():
    return Author.objects.all()
