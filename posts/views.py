import requests
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import authentication
from rest_framework import status, serializers
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.response import Response
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import LoginUser
from .forms import RegisterUser

from posts.models import Post, Comment


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


class GetPostShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title']


class GetCommentsSerializer(serializers.ModelSerializer):
    user = UsersSerializer(read_only=True)
    post = GetPostShortSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user']


class GetCommentByIdSerializer(serializers.ModelSerializer):
    user = UsersSerializer(read_only=True)
    post = GetPostShortSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'text', 'user', 'date_created', 'date_updated']


class AddCommentSerializer(serializers.ModelSerializer):
    user = UsersSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'post', 'user']


class PutCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text']


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


class Comments(ListCreateAPIView):
    model = Comment
    authentication_classes = [authentication.TokenAuthentication]

    @extend_schema(
        request=GetCommentsSerializer,
        responses=GetCommentsSerializer,
    )
    def list(self, request):
        all_comments = Comment.objects.all()
        serializer = GetCommentsSerializer(all_comments, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=AddCommentSerializer,
        responses=AddCommentSerializer,
    )
    def post(self, args, **kwargs):
        try:
            text = self.request.data.get('text', '')
            post_id = self.request.data.get('post', '')
            post = get_object_or_404(Post, pk=post_id)
            serializer = AddCommentSerializer(data=self.request.data)
            serializer.is_valid(raise_exception=True)
            return self.insert_comment([text, post, self.request.user])
        except Exception:
            return Response(data={'message': 'Failed to create object!'}, status=status.HTTP_400_BAD_REQUEST)

    def insert_comment(self, data):
        comment = Comment.objects.create(text=data[0], post=data[1], user=data[2])
        return Response(data=AddCommentSerializer(comment).data, status=status.HTTP_201_CREATED)


class CommentById(ListAPIView):
    model = Comment
    authentication_classes = [authentication.TokenAuthentication]

    @extend_schema(
        request=GetCommentByIdSerializer,
        responses=GetCommentByIdSerializer,
    )
    def list(self, request, **kwargs):
        comment_id = kwargs['id']
        comment = get_object_or_404(Comment, id=comment_id)
        serializer = GetCommentByIdSerializer(comment)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=PutCommentSerializer,
        responses=PutCommentSerializer,
    )
    def put(self, request, **kwargs):
        try:
            comment_id = kwargs['id']
            comment = get_object_or_404(Comment, id=comment_id)
            serializer = PutCommentSerializer(comment, data=request.data)
            if serializer.is_valid() and request.user == comment.user:
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            raise ValueError
        except ValueError:
            return Response(data={'message': 'Failed to update object!'}, status=status.HTTP_400_BAD_REQUEST)


def home_view(request):
    all_posts = Post.objects.all().order_by('-date_updated')[:5]
    context = {
        'posts': all_posts,
        'user': request.user if request.user.is_authenticated else None,
    }

    html_string = render_to_string('posts/home.html', context=context)
    return HttpResponse(html_string)


def contact_view(request):
    all_posts = Post.objects.all()
    context = {
        'posts': all_posts,
        'user': request.user if request.user.is_authenticated else None,
    }

    html_string = render_to_string('posts/contact.html', context=context)
    return HttpResponse(html_string)


@login_required
def profile_view(request):
    context = {
        'api_key': request.session.get('token', ''),
        'user': request.user,
        'posts': Post.objects.filter(user=request.user).order_by('-date_updated'),
    }
    return render(request, 'posts/profile.html', context=context)


def posts_view(request):
    sort = request.GET.get('sort', '')

    if sort == 'creator':
        all_posts = Post.objects.select_related('user').order_by('user')
    elif sort == 'date_ascending':
        all_posts = Post.objects.select_related('user').order_by('date_created')
    elif sort == 'date_descending':
        all_posts = Post.objects.select_related('user').order_by('-date_created')
    elif sort == 'title':
        all_posts = Post.objects.select_related('user').order_by('title')
    else:
        all_posts = Post.objects.select_related('user').order_by('-date_created')

    context = {
        'posts': all_posts,
        'user': request.user if request.user.is_authenticated else None,
    }

    return render(request, 'posts/posts_list.html', context=context)


def post_view(request, id):
    post = Post.objects.get(id=id)
    context = {
        'post': post,
        'id': id,
        'comments': Comment.objects.select_related('post', 'user').filter(post=id),
    }
    return render(request, 'posts/post.html', context=context)


def create_post(request):
    title = request.POST.get('title', '')
    body = request.POST.get('body', '')

    if title is None:
        context = {
            'error': 'Title cannot be empty.',
            'posts': Post.objects.select_related('user'),
            'title': title,
            'body': body,
        }
        return render(request, 'posts/posts_list.html', context)

    if len(body) < 50:
        context = {
            'error': 'Body has to be at least 50 characters long.',
            'posts': Post.objects.select_related('user'),
            'title': title,
            'body': body,
        }
        return render(request, 'posts/posts_list.html', context)

    post = Post(title=title, body=body, user_id=request.user.id)
    post.save()

    context = {
        'message': 'Post created successfully!',
        'posts': Post.objects.select_related('user'),
    }

    return render(request, 'posts/posts_list.html', context)


def create_comment(request):
    text = request.POST.get('text', '')
    post_id = request.POST.get('id', ''),
    post_id = post_id[0]

    if text:
        comment = Comment(
            text=text,
            post=Post.objects.get(pk=post_id),
            user=request.user,
        )
        comment.save()

        context = {
            'post': Post.objects.get(id=post_id),
            'id': post_id,
            'message': 'Your comment has been posted.',
            'comments': Comment.objects.select_related('post', 'user').filter(post=post_id)
        }

        return render(request, 'posts/post.html', context)
    else:
        context = {
            'post': Post.objects.get(id=post_id),
            'id': post_id,
            'error': 'Cannot post empty comment.',
        }
        return render(request, 'posts/post.html', context)


def login_register_view(request):
    return render(request, 'posts/login.html')


@csrf_protect
def create_user(request):
    if request.POST.get('password-reg') == request.POST.get('confirm-password') and len(
            request.POST.get('password-reg')) >= 8:
        user = User.objects.create_user(
            request.POST.get('username-reg', ''),
            request.POST.get('email-reg', ''),
            request.POST.get('password-reg', '')
        )
        user.save()

        login(request, user)
        result = requests.post('http://127.0.0.1:8000/api-token-auth/',
                               json={
                                   'username': request.POST.get('username-reg', ''),
                                   'password': request.POST.get('password-reg', '')
                               })

        request.session['token'] = result.json()['token']

        context = {
            'api_key': request.session.get('token', ''),
            'user': user,
        }

        return render(request, 'posts/profile.html', context)
    else:
        context = {
            'error': 'Error! Passwords do not match!',
        }
        return render(request, 'posts/login.html', context)


@csrf_protect
def login_user(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        result = requests.post('http://127.0.0.1:8000/api-token-auth/',
                               json={'username': username, 'password': password})
        request.session['token'] = result.json()['token']
        context = {
            'api_key': request.session.get('token', ''),
            'user': user,
            'posts': Post.objects.filter(user=request.user).order_by('-date_updated'),
        }
        return render(request, 'posts/profile.html', context)
    else:
        context = {
            'error': 'Error! Invalid username or password!',
        }
        return render(request, 'posts/login.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def password_reset(request):
    user = request.user
    password_old_input = request.POST.get('password_old', '')
    password_new1 = request.POST.get('password_new1', '')
    password_new2 = request.POST.get('password_new2', '')

    if len(password_old_input) < 8:
        context = {
            'user': user,
            'error': 'Failed to change password! Password must be at least 8 characters long.'
        }
        return render(request, 'posts/profile.html', context)

    if password_new1 == password_new2:
        password = password_new1
    else:
        context = {
            'user': user,
            'error': 'Failed to change password! Passwords do not match.'
        }
        return render(request, 'posts/profile.html', context)

    if authenticate(username=user.username, password=password_old_input):
        user.set_password(password)
        user.save()

        context = {
            'user': user,
            'message': 'Password has been changed successfully.'
        }

        return render(request, 'posts/profile.html', context)
    else:
        context = {
            'user': user,
            'error': 'Failed to change password! Current password is incorrect.'
        }
        return render(request, 'posts/profile.html', context)


@csrf_exempt
def update_comment(request, id):
    post_id = request.POST.get('post_id', '')
    comment = Comment.objects.get(pk=id)
    text = request.POST.get('comment', comment.text)
    comment.text = text
    comment.save()

    context = {
        'post': Post.objects.get(id=post_id),
        'id': post_id,
        'comments': Comment.objects.select_related('post', 'user').filter(post=post_id)
    }

    return render(request, 'posts/post.html', context)
