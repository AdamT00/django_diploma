from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.Posts.as_view(), name='posts'),
    path('<int:id>/', views.PostById.as_view(), name='post_by_id'),
    re_path('post/(?P<id>-*[0-9]+)/\\Z', views.PostById.as_view(), name='post_by_id'),
]
