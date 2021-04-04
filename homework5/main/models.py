from django.db import models
from django.utils.timezone import now


class Author(models.Model):
    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    name = models.CharField("Author name", max_length=100)
    email = models.EmailField("Author email", max_length=100)

    def __str__(self):
        return f"ID {self.id} - {self.name}"


class Subscriber(models.Model):
    email_to = models.EmailField("Subscriber email", max_length=100)
    author_id = models.ForeignKey("Author", on_delete=models.CASCADE)

    def __str__(self):
        return self.email_to


class Post(models.Model):
    class Meta:
        db_table = "table_posts"
        ordering = ['-id']

    title = models.CharField("Post title", max_length=100)
    description = models.CharField("Post description", max_length=50)
    content = models.TextField("Post content", max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=now)

    def __str__(self):
        return self.title

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'content': self.content,
            'created': self.created,
        }
