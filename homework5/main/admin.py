from django.contrib import admin

from .models import Post, User


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'content', 'created']
    search_fields = ['title', 'description', 'content']

    class Meta:
        model = Post


admin.site.register(Post, PostAdmin)
admin.site.register(User)
