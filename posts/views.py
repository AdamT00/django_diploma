from django.shortcuts import render
from django.http import HttpResponse
from posts.models import Post
from rest_framework import generics, status
from rest_framework.response import Response
import datetime
from rest_framework.views import APIView
from rest_framework import authentication, permissions


class AddPost(APIView):
    model = Post

    authentication_classes = [authentication.TokenAuthentication]

    # working with kwargs - probably not the right solution
    def post(self, args, **kwargs):
        title = kwargs['title']
        body = kwargs['body']
        self.insert_post([title, body])
        return Response(data={'title': title, 'body': body}, status=status.HTTP_200_OK)

    # not working with request - need help with this
    # def post(self, request):
    #     title = request.POST.get('title', '')
    #     body = request.POST.get('body', '')
    #     return Response(data={'title': title, 'body': body}, status=status.HTTP_200_OK)

    def insert_post(self, data):
        Post.objects.create(title=data[0], body=data[1])
        return Response(data={'message': 'Post added successfully!'}, status=status.HTTP_200_OK)
