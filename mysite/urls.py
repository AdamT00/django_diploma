from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken import views

from posts import views as post_views


urlpatterns = [
    path('', post_views.home_view),
    path('home/', post_views.home_view),
    path('contact/', post_views.contact_view),
    path('posts/', post_views.posts_view),
    path('profile/', post_views.profile_view),
    path('login-register/', post_views.login_register_view),
    path('create-user/', post_views.create_user),
    path('login-user/', post_views.login_user),

    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('users/', include('users.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    path('post/', include('posts.urls')),
]
