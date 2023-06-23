from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    fields = ['title', 'body', 'user']


admin.site.register(Post, PostAdmin)
