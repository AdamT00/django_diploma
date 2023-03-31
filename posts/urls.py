from django.urls import path

from . import views

urlpatterns = [
    path('', views.Posts.as_view(), name='posts'),
    path('<int:id>/', views.PostById.as_view(), name='post_by_id'),
]
