from django.core.management import BaseCommand
from django.db import IntegrityError
from faker import Faker
from main.models import Author, Book, Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker()
        for _ in range(50):
            try:
                Author(name=fake.name(), email=fake.email()).save()
            except IntegrityError:
                pass
        for _ in range(10):
            try:
                Category(title=fake.cryptocurrency_name()).save()
            except IntegrityError:
                pass
        for i in range(200):
            author = Author.objects.all().order_by('?').last()
            category = Category.objects.all().order_by('?').last()
            try:
                Book(title=f'Title {i}', author_id=author, category_id=category).save()
            except IntegrityError:
                pass
