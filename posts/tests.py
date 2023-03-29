from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from posts.models import Post


class TestCase(APITestCase):
    client_class = APIClient

    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                             email='testUser@example.com',
                                             is_superuser=1,
                                             is_staff=1,
                                             is_active=1,
                                             password='password')
        Token.objects.create(user=self.user)
        super(TestCase, self).setUp()


class TestPostCreation(TestCase):
    def test_post_creation(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        sample_data = {'title': 'Sample title', 'body': 'Sample content'}
        response = self.client.post(reverse('posts'), sample_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], sample_data['title'])
        self.assertEqual(response.data['body'], sample_data['body'])

    def test_post_creation_negative(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        sample_data = {'title': 'Sample title that contains more than thirty characters', 'body': 'Sample content'}
        response = self.client.post(reverse('posts'), sample_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestGetPostFromId(TestCase):
    def test_get_post_from_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)

        self.post = Post.objects.create(id=1, title='Title of the post', body='Body of the post', user=self.user)
        self.post = Post.objects.create(id=20, title='Title of the post', body='Body of the post', user=self.user)
        self.post = Post.objects.create(title='Title of the post', body='Body of the post', user=self.user)

        post_id = 2
        response = self.client.get(f'/posts/{post_id}')
        print(response.__dict__)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
