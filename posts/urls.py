from django.urls import path
from . import views

urlpatterns = [
    path('', views.AddPost.as_view(), name='add_post'),
]