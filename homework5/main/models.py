from django.db import models
from django.utils.timezone import now


class User(models.Model):
    class Meta:
        db_table = "table_users"

    name = models.CharField("User name", max_length=100)
    email = models.EmailField("User email", max_length=100)

    def __str__(self):

        return self.name


class Post(models.Model):
    class Meta:
        db_table = "table_post"
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
