from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from posts.models import Post


class TestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                             email='testUser@example.com',
                                             is_superuser=1,
                                             is_staff=1,
                                             is_active=1,
                                             password='password')
        Token.objects.create(user=self.user)
        self.post1 = Post.objects.create(title='Title of the post', body='Body of the post', user=self.user)
        super(TestCase, self).setUp()

    def test_can_read_user_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        response = self.client.get(reverse('post_by_id', kwargs={'id': self.post1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
