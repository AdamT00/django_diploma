from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User

user = User.objects.create_user(username='adam3', email='tolcseradam@gmail.com', password='password')

class AuthView(generics.GenericAPIView):
    def authenticate_user(self):
        return True

    def get(self, request):
        return Response(data={'message': 'Hello Auth', 'name': 'asd'}, status=status.HTTP_200_OK)

