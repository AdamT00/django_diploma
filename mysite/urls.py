from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken import views

from posts import views as post_views


urlpatterns = [
    path('', post_views.home_view, name='home'),
    path('home/', post_views.home_view, name='home'),
    path('contact/', post_views.contact_view, name='contact'),
    path('posts/', post_views.posts_view),
    path('blog-post/<int:id>/', post_views.post_view, name='blog-post'),
    path('create-post/', post_views.create_post, name='create-post'),
    path('profile/', post_views.profile_view, name='profile'),
    path('login-register/', post_views.login_register_view, name='login-register'),
    path('create-user/', post_views.create_user, name='register-user'),
    path('login/', post_views.login_user, name='login-user'),
    path('logout/', post_views.logout_view, name='logout-user'),
    path('password-reset/', post_views.password_reset, name='password-reset'),
    path('create-comment/', post_views.create_comment, name='create-comment'),

    path('accounts/', include("django.contrib.auth.urls")),
    path('accounts/login/', auth_views.LoginView.as_view),

    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('users/', include('users.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    path('post/', include('posts.urls')),
]
