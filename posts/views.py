from django.shortcuts import render
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema

from posts.models import Post
from rest_framework import generics, status, serializers
from rest_framework.response import Response
import datetime
from rest_framework.views import APIView
from rest_framework import authentication, permissions


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'body']


class AddPost(APIView):
    model = Post

    authentication_classes = [authentication.TokenAuthentication]

    @extend_schema(
        request=PostSerializer,
        responses=PostSerializer,
    )
    def post(self, args, **kwargs):
        title = self.request.data.get('title', '')
        body = self.request.data.get('body', '')
        return self.insert_post([title, body])

    def insert_post(self, data):
        Post.objects.create(title=data[0], body=data[1])
        return Response(data={'message': 'Post added successfully!'}, status=status.HTTP_200_OK)


