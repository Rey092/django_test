from main.models import Author


def get_all_authors():
    return Author.objects.all()
