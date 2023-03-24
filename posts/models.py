from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField
    date_created = models.DateTimeField
    date_updated = models.DateTimeField
