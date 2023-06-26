from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import authentication
from rest_framework import status, serializers
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.response import Response
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from .forms import LoginUser
from .forms import RegisterUser


from posts.models import Post


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class AddPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'body']


class GetPostSerializer(serializers.ModelSerializer):
    user = UsersSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'date_created', 'date_updated', 'user']


class GetPostByIdSerializer(serializers.ModelSerializer):
    user = UsersSerializer()

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'date_created', 'date_updated', 'user']


class PutPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'body']


class Posts(ListCreateAPIView):
    model = Post
    authentication_classes = [authentication.TokenAuthentication]

    @extend_schema(
        request=GetPostSerializer,
        responses=GetPostSerializer,
    )
    def list(self, args, **kwargs):
        all_posts = Post.objects.all()
        serializer = GetPostSerializer(all_posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=AddPostSerializer,
        responses=AddPostSerializer,
    )
    def post(self, args, **kwargs):
        try:
            title = self.request.data.get('title', '')
            body = self.request.data.get('body', '')
            user_id = self.request.user.id
            serializer = AddPostSerializer(data={'title': title, 'body': body})
            serializer.is_valid(raise_exception=True)
            return self.insert_post([title, body, user_id])
        except Exception:
            return Response(data={'message': 'Failed to create object!'}, status=status.HTTP_400_BAD_REQUEST)

    def insert_post(self, data):
        post = Post.objects.create(title=data[0], body=data[1], user_id=data[2])
        return Response(data=AddPostSerializer(post).data, status=status.HTTP_201_CREATED)


class PostById(ListAPIView):
    model = Post
    authentication_classes = [authentication.TokenAuthentication]

    def list(self, request, **kwargs):
        post_id = kwargs['id']
        post = get_object_or_404(Post, id=post_id)
        serializer = GetPostByIdSerializer(post)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=PutPostSerializer,
        responses=PutPostSerializer,
    )
    def put(self, request, **kwargs):
        try:
            post_id = kwargs['id']
            post = get_object_or_404(Post, id=post_id)
            serializer = PutPostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            raise ValueError
        except ValueError:
            return Response(data={'message': 'Failed to update object!'}, status=status.HTTP_400_BAD_REQUEST)


def home_view(request):
    current_user = request.user
    all_posts = Post.objects.all()
    context = {
        'posts': all_posts[:5],
        'user': current_user.email,
    }

    html_string = render_to_string("posts/home.html", context=context)
    return HttpResponse(html_string)


def contact_view(request):
    current_user = request.user
    all_posts = Post.objects.all()
    context = {
        'posts': all_posts,
        'user': current_user.email,
    }

    html_string = render_to_string("posts/contact.html", context=context)
    return HttpResponse(html_string)


def profile_view(request):
    if request.user.is_authenticated:
        return render(request, 'posts/profile.html')
    else:
        return render(request, 'posts/login_register.html')


def posts_view(request):
    current_user = request.user
    all_posts = Post.objects.all()
    context = {
        'posts': all_posts,
        'user': current_user.email,
    }

    html_string = render_to_string("posts/posts_list.html", context=context)
    return HttpResponse(html_string)


def login_register_view(request):

    context = {
    }

    return render(request, "posts/login_register.html")


@csrf_protect
def create_user(request):
    if request.POST.get('password-reg') == request.POST.get('confirm-password') and len(request.POST.get('password-reg')) >= 8:
        user = User.objects.create_user(
            request.POST.get('username-reg', ''),
            request.POST.get('email-reg', ''),
            request.POST.get('password-reg', '')
        )
        user.save()
        return render(request, 'posts/profile.html')
    else:
        context = {
            'error': 'Error! Passwords dont match!',
        }
        return render(request, 'posts/login_register.html', context)


@csrf_protect
def login_user(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        context = {
            'username': username,
            'password': password,
            'user': user,
        }
        return render(request, 'posts/profile.html', context)
    else:
        context = {
            'error': 'Error! Invalid username or password!',
        }
        return render(request, 'posts/login_register.html', context)



