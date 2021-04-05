from django.contrib import admin

from .models import Author, Post, Subscriber


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'content', 'created']
    search_fields = ['title', 'description', 'content']

    class Meta:
        model = Post


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'email']

    class Meta:
        model = Author


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email_to', 'id', 'author_id']
    search_fields = ['author_id', 'email_to']

    class Meta:
        model = Subscriber


admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
