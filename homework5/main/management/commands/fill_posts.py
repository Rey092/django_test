from django.core.exceptions import ValidationError
from django.core.management import BaseCommand
from django.db import IntegrityError
from main.models import Author, Post
from main.services.scraper import medusweet_scraper


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = medusweet_scraper()
        titles = data['titles']
        contents = data['contents']
        for title, content in zip(titles, contents):
            try:
                post = Post(
                    author_id=Author.objects.order_by('?').last(),
                    title=title,
                    description='No description',
                    content=content,
                )
                post.full_clean()
            except IntegrityError:
                pass
            except ValidationError:
                print(ValidationError)
            else:
                post.save()
