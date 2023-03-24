from django.urls import path
from . import views

urlpatterns = [
    path('<str:title>/<str:body>', views.AddUser.as_view(), name='Add User'),
]