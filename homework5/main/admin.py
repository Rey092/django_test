from django.contrib import admin

from .models import Author, Logger, Post, Subscriber


class PostAdmin(admin.ModelAdmin):
    list_display = ["id", 'title', 'description', 'content', 'created']
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


class LoggerAdmin(admin.ModelAdmin):
    list_display = ['path', 'user_ip', 'time_execution', 'utm', 'created']

    class Meta:
        model = Logger


admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Logger, LoggerAdmin)
