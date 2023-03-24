from django.shortcuts import render
from django.http import HttpResponse
from posts.models import Post
from rest_framework import generics, status
from rest_framework.response import Response


class AddUser(generics.GenericAPIView):
    model = Post

    def post(self, request):
        request.POST.get('title', '')
        request.POST.get('body', '')
        return Response(data={'message': 'asd'}, status=status.HTTP_200_OK)
