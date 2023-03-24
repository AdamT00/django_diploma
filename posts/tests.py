from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class TestCase(APITestCase):
    def test_posts(self):
        response = self.client.post('/post/')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Object created!')

    def test_post_creation(self):
        sample_data = {'title': 'Sample title', 'body': 'Sample content'}
        response = self.client.post(reverse('add_post'), sample_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], sample_data['title'])
