from django.urls import path
from . import views

urlpatterns = [
    path('<str:title>/<str:body>', views.AddPost.as_view(), name='Add Post'),
]