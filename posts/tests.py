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
        super(TestCase, self).setUp()

    def test_read_post_detail(self):
        self.post1 = Post.objects.create(title='Title of the post', body='Body of the post', user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        response = self.client.get(reverse('post_by_id', kwargs={'id': self.post1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.post1.title)
        self.assertEqual(response.data['body'], self.post1.body)
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['username'], self.user.username)

    def test_read_post_detail_negative(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        response = self.client.get(reverse('post_by_id', kwargs={'id': 2}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

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

    def test_post_update(self):
        self.post1 = Post.objects.create(title='Title of the post', body='Body of the post', user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        sample_data = {'title': 'Sample title', 'body': 'Sample content'}
        response = self.client.put(
            reverse('post_by_id', kwargs={'id': self.post1.id}),
            data=sample_data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.post1.id)
        self.assertEqual(response.data['title'], sample_data['title'])
        self.assertEqual(response.data['body'], sample_data['body'])

    def test_post_update_negative(self):
        self.post1 = Post.objects.create(title='Title of the post', body='Body of the post', user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        response = self.client.put(
            reverse('post_by_id', kwargs={'id': self.post1.id}),
            data={'title': 'Sample title', 'body': ''},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
