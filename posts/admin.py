from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user']
    list_filter = ['user']
    search_fields = ['title', 'user__username']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'post', 'user']
    list_filter = ['post', 'user']
    search_fields = ['text', 'post__title', 'user__username']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
