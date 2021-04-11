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

    def serialize(self):
        return {
            'author_id': self.id,
            'author_name': self.name,
            'author_email': self.email,
        }


class Subscriber(models.Model):
    class Meta:
        unique_together = [("email_to", "author_id")]
        ordering = ['-id']

    email_to = models.EmailField("Subscriber email", max_length=100)
    author_id = models.ForeignKey("Author", on_delete=models.CASCADE)

    def __str__(self):
        return self.email_to

    def serialize(self):
        return {
            'id': self.id,
            'email_to': self.email_to,
            'author_id': self.author_id.id,
            'author_name': self.author_id.name,
            'author_email': self.author_id.email,
        }


class Post(models.Model):
    class Meta:
        db_table = "table_posts"
        ordering = ['-id']

    author_id = models.ForeignKey("Author", on_delete=models.CASCADE)
    title = models.CharField("Post title", max_length=100)
    description = models.CharField("Post description", max_length=50)
    content = models.TextField("Post content", max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=now)

    def __str__(self):
        return self.title

    def serialize(self):
        return {
            'id': self.id,
            'author_id': self.author_id.id,
            'author_name': self.author_id.name,
            'author_email': self.author_id.email,
            'title': self.title,
            'description': self.description,
            'content': self.content,
            'created': self.created,
            'updated': self.updated,
        }


class Comment(models.Model):
    class Meta:
        ordering = ['-id']

    content = models.TextField("Post content", max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    post_id = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Logger(models.Model):
    path = models.CharField(max_length=100)
    user_ip = models.GenericIPAddressField(max_length=20)
    time_execution = models.DecimalField(max_digits=10, decimal_places=7)
    utm = models.CharField(max_length=500, null=True)
    created = models.DateTimeField(auto_now_add=True)
