from django.db import models
from rest_framework.authtoken.admin import User


class Post(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField(default='')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
