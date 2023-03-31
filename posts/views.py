from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.utils import extend_schema
from rest_framework import authentication
from rest_framework import status, serializers
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.response import Response

from posts.models import Post


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class AddPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'body']


class PutPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'body']

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('title', instance.title)


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
        Post.objects.create(title=data[0], body=data[1], user_id=data[2])
        return Response(data={'message': 'Object created!', 'title': data[0], 'body': data[1]},
                        status=status.HTTP_201_CREATED)

    @extend_schema(
        request=PutPostSerializer,
        responses=PutPostSerializer,
    )
    def put(self, args, **kwargs):
        try:
            # id = kwargs['id']
            title = self.request.data.get('title', '')
            body = self.request.data.get('body', '')
            if id is not None:
                post = Post.objects.get(id=id)
                serializer = PutPostSerializer(post, data={'title': title, 'body': body})
                if serializer.is_valid():
                    serializer.save()
                    return Response(data={'message': 'Updated successfully!'})

            # post_id = self.request.body
            # serializer = AddPostSerializer(data={'id': post_id})
            # serializer.is_valid(raise_exception=True)
            # return Response(data={'post': post_id}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(data={'message': 'Failed to update object!'}, status=status.HTTP_400_BAD_REQUEST)


class PostById(ListAPIView):
    model = Post
    authentication_classes = [authentication.TokenAuthentication]

    def list(self, request, **kwargs):
        try:
            post_id = kwargs['id']
            post = Post.objects.get(id=post_id)
            serializer = GetPostByIdSerializer(post)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(data={'message': 'Object does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
