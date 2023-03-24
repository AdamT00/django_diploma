from django.shortcuts import render
from django.http import HttpResponse
from posts.models import Post
from rest_framework import generics, status
from rest_framework.response import Response


class AddUser(generics.GenericAPIView):
    model = Post

    def post(self, args, **kwargs):
        title = kwargs['title']
        body = kwargs['body']
        # title = request.POST.get('title')
        # body = request.POST.get('body')
        return Response(data={'title': title, 'body': body}, status=status.HTTP_200_OK)
