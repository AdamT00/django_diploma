from django.http import HttpResponse
from drf_spectacular.utils import extend_schema
from rest_framework import authentication
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post


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
        try:
            title = self.request.data.get('title', '')
            body = self.request.data.get('body', '')
            user_id = self.request.user
            serializer = PostSerializer(data={'title': title, 'body': body})
            serializer.is_valid(raise_exception=True)
            return self.insert_post([title, body, user_id])
        except Exception:
            print('The title is too long or too short.')
            return Response(data={'message': 'Failed to create object!'}, status=status.HTTP_400_BAD_REQUEST)


    def insert_post(self, data):
        Post.objects.create(title=data[0], body=data[1], user_id=data[2])
        return Response(data={'message': 'Object created!', 'title': data[0], 'body': data[1]},
                        status=status.HTTP_201_CREATED)
