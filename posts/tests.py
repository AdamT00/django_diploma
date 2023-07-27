from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from posts.models import Post, Comment


class TestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                             email='testUser@example.com',
                                             is_superuser=1,
                                             is_staff=1,
                                             is_active=1,
                                             password='password')
        self.user2 = User.objects.create_user(username='test_user2', email='testUser2@example.com', password='password')
        Token.objects.create(user=self.user)
        Token.objects.create(user=self.user2)
        super(TestCase, self).setUp()

    def test_read_all_posts(self):
        self.post1 = Post.objects.create(title='Title of post one', body='Body of the post', user=self.user)
        self.post2 = Post.objects.create(title='Title of post two', body='Body of the post', user=self.user)
        self.post3 = Post.objects.create(title='Title of post three', body='Body of the post', user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        response = self.client.get(reverse('posts'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0]['title'], self.post1.title)
        self.assertEqual(response.data[1]['title'], self.post2.title)
        self.assertEqual(response.data[2]['title'], self.post3.title)

        for i in range(3):
            self.assertEqual(response.data[i]['user']['id'], self.user.id)
            self.assertEqual(response.data[i]['user']['username'], self.user.username)

    def test_read_post_detail(self):
        self.post1 = Post.objects.create(title='Title of the post', body='Body of the post', user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        response = self.client.get(reverse('post_by_id', kwargs={'id': self.post1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.post1.title)
        self.assertEqual(response.data['body'], self.post1.body)
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['username'], self.user.username)

    def test_read_post_detail_wrong_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        response = self.client.get(reverse('post_by_id', kwargs={'id': 123}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_post_detail_negative_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        response = self.client.get(reverse('post_by_id', kwargs={'id': -1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_creation(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        sample_data = {'title': 'Sample title', 'body': 'Sample content'}
        response = self.client.post(reverse('posts'), sample_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], Post.objects.last().id)
        self.assertEqual(response.data['title'], sample_data['title'])
        self.assertEqual(response.data['body'], sample_data['body'])

    def test_post_creation_title_too_long(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        sample_data = {'title': 'Sample title that contains more than thirty characters', 'body': 'Sample content'}
        response = self.client.post(reverse('posts'), sample_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_creation_title_empty(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        sample_data = {'title': '', 'body': 'Sample content'}
        response = self.client.post(reverse('posts'), sample_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_creation_body_empty(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        sample_data = {'title': 'Sample title', 'body': ''}
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

    def test_post_update_empty_body(self):
        self.post1 = Post.objects.create(title='Title of the post', body='Body of the post', user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        response = self.client.put(
            reverse('post_by_id', kwargs={'id': self.post1.id}),
            data={'title': 'Sample title', 'body': ''},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_update_empty_title(self):
        self.post1 = Post.objects.create(title='Title of the post', body='Body of the post', user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        response = self.client.put(
            reverse('post_by_id', kwargs={'id': self.post1.id}),
            data={'title': '', 'body': 'Sample body'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_update_title_too_long(self):
        self.post1 = Post.objects.create(title='Title of the post', body='Body of the post', user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        response = self.client.put(
            reverse('post_by_id', kwargs={'id': self.post1.id}),
            data={'title': 'Sample title that contains more than thirty characters lorem ipsum', 'body': 'Sample body'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_update_wrong_id(self):
        self.post1 = Post.objects.create(title='Title of the post', body='Body of the post', user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        response = self.client.put(
            reverse('post_by_id', kwargs={'id': 123}),
            data={'title': 'Sample title', 'body': 'Sample body'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_update_negative_id(self):
        self.post1 = Post.objects.create(title='Title of the post', body='Body of the post', user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        response = self.client.put(
            reverse('post_by_id', kwargs={'id': -1}),
            data={'title': 'Sample title', 'body': 'Sample body'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_all_comments(self):
        self.post = Post.objects.create(title='Title of post one', body='Body of the post', user=self.user)

        self.comment1 = Comment.objects.create(text='Text of comment one.', post=self.post, user=self.user)
        self.comment2 = Comment.objects.create(text='Text of comment two.', post=self.post, user=self.user)
        self.comment3 = Comment.objects.create(text='Text of comment three.', post=self.post, user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        response = self.client.get(reverse('comments'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for i in range(3):
            self.assertIn(response.data[i]['id'], [self.comment1.id, self.comment2.id, self.comment3.id])
            self.assertEqual(response.data[i]['post']['id'], self.post.id)
            self.assertEqual(response.data[i]['post']['title'], self.post.title)
            self.assertEqual(response.data[i]['user']['id'], self.user.id)
            self.assertEqual(response.data[i]['user']['username'], self.user.username)

    def test_read_comment_detail(self):
        self.post = Post.objects.create(title='Title of the post', body='Body of the post', user=self.user)
        self.comment = Comment.objects.create(text='Text of comment one.', post=self.post, user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        response = self.client.get(reverse('comment_by_id', kwargs={'id': self.comment.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['id'], self.comment.id)
        self.assertEqual(response.data['post']['id'], self.post.id)
        self.assertEqual(response.data['post']['title'], self.post.title)
        self.assertEqual(response.data['text'], self.comment.text)
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['username'], self.user.username)

    def test_read_comment_detail_wrong_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        response = self.client.get(reverse('comment_by_id', kwargs={'id': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_comment_detail_negative_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        response = self.client.get(reverse('comment_by_id', kwargs={'id': -1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_creation(self):
        self.post = Post.objects.create(title='Title of the post', body='Body of the post', user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        sample_data = {
            "text": "Sample Text",
            "post": self.post.id
        }
        response = self.client.post(reverse('comments'), sample_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], Comment.objects.last().id)
        self.assertEqual(response.data['text'], sample_data['text'])
        self.assertEqual(response.data['post'], sample_data['post'])
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['username'], self.user.username)

    def test_comment_creation_post_does_not_exist(self):
        self.post = Post.objects.create(title='Title of the post', body='Body of the post', user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        sample_data = {
            "text": "Sample Text",
            "post": 999
        }
        response = self.client.post(reverse('comments'), sample_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Failed to create object!')

    def test_comment_creation_post_negative_id(self):
        self.post = Post.objects.create(title='Title of the post', body='Body of the post', user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        sample_data = {
            "text": "Sample Text",
            "post": -1
        }
        response = self.client.post(reverse('comments'), sample_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Failed to create object!')

    def test_comment_update(self):
        self.post = Post.objects.create(title='Title of the post', body='Body of the post', user=self.user)
        self.comment = Comment.objects.create(text='Original text of the comment', post=self.post, user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        sample_data = {'text': 'Sample text'}
        response = self.client.put(
            reverse('comment_by_id', kwargs={'id': self.comment.id}),
            data=sample_data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.comment.id)
        self.assertEqual(response.data['text'], sample_data['text'])

    def test_comment_update_empty_text(self):
        self.post = Post.objects.create(title='Title of the post', body='Body of the post', user=self.user)
        self.comment = Comment.objects.create(text='Original text of the comment', post=self.post, user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        sample_data = {'text': ''}
        response = self.client.put(
            reverse('comment_by_id', kwargs={'id': self.comment.id}),
            data=sample_data,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_update_id_doesnt_exist(self):
        self.post = Post.objects.create(title='Title of the post', body='Body of the post', user=self.user)
        self.comment = Comment.objects.create(text='Original text of the comment', post=self.post, user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        sample_data = {'text': 'Sample text'}
        response = self.client.put(
            reverse('comment_by_id', kwargs={'id': 9999}),
            data=sample_data,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')

    def test_comment_update_wrong_user(self):
        self.post = Post.objects.create(title='Title of the post', body='Body of the post', user=self.user)
        self.comment = Comment.objects.create(text='Original text of the comment', post=self.post, user=self.user2)
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        sample_data = {'text': 'Sample text'}
        response = self.client.put(
            reverse('comment_by_id', kwargs={'id': self.comment.id}),
            data=sample_data,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Failed to update object!')

    def test_comment_update_negative_id(self):
        self.post = Post.objects.create(title='Title of the post', body='Body of the post', user=self.user)
        self.comment = Comment.objects.create(text='Original text of the comment', post=self.post, user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.auth_token.key)
        sample_data = {'text': 'Sample text'}
        response = self.client.put(
            reverse('comment_by_id', kwargs={'id': -1}),
            data=sample_data,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')
