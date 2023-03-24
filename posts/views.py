from drf_spectacular.utils import extend_schema
from rest_framework import authentication
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

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
        title = self.request.data.get('title', '')
        body = self.request.data.get('body', '')
        # user_id =
        return self.insert_post([title, body])

    def insert_post(self, data):
        Post.objects.create(title=data[0], body=data[1])
        return Response(data={'message': 'Object created!', 'title': data[0]}, status=status.HTTP_201_CREATED)
