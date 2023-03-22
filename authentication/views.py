from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response


class AuthView(generics.GenericAPIView):
    def authenticate_user(self):
        return True

    def get(self, request):
        return Response(data={'message': 'Hello Auth', 'name': 'asd'}, status=status.HTTP_200_OK)
