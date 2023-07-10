from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    fields = ['title', 'body', 'user']


class CommentAdmin(admin.ModelAdmin):
    fields = ['text', 'post', 'user']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
