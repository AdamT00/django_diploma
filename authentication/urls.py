from django.urls import path
from . import views

urlpatterns = [
    path('', views.AuthView.as_view(), name='hello_auth'),
    path('users/', views.AuthView.as_view(), name='users'),
    # path('?name=<str:name>/?password=<str:password>', views.AuthView.as_view(), name='user_authentication'),
]
