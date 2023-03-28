from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema
from rest_framework import authentication
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

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


class Posts(APIView):
    model = Post
    authentication_classes = [authentication.TokenAuthentication]

    @extend_schema(
        request=GetPostSerializer,
        responses=GetPostSerializer,
    )
    def get(self, args, **kwargs):
        all_posts = Post.objects.all()
        serializer = GetPostSerializer(all_posts, many=True)
        return Response(data={'message': serializer.data}, status=status.HTTP_200_OK)

    @extend_schema(
        request=AddPostSerializer,
        responses=AddPostSerializer,
    )
    def post(self, args, **kwargs):
        try:
            title = self.request.data.get('title', '')
            body = self.request.data.get('body', '')
            user_id = self.request.user
            serializer = AddPostSerializer(data={'title': title, 'body': body})
            serializer.is_valid(raise_exception=True)
            return self.insert_post([title, body, user_id])
        except Exception:
            print('The title is too long or too short.')
            return Response(data={'message': 'Failed to create object!'}, status=status.HTTP_400_BAD_REQUEST)

    def insert_post(self, data):
        Post.objects.create(title=data[0], body=data[1], user_id=data[2])
        return Response(data={'message': 'Object created!', 'title': data[0], 'body': data[1]},
                        status=status.HTTP_201_CREATED)
