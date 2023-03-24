from django.urls import path
from . import views

urlpatterns = [
    path('', views.AddPost.as_view(), name='Add Post'),
]