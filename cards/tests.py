from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Card


class CardAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.client.force_authenticate(user=self.user)

    def test_create_card_validations(self):
        data = {'ccv': 9999, 'card_number': '1234567890123456', 'title': 'Test Card'}
        response = self.client.post('/cards/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'ccv': 123, 'card_number': '1234', 'title': 'Test Card'}
        response = self.client.post('/cards/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'ccv': 123, 'card_number': '1234567890123456', 'title': 'Test Card'}
        response = self.client.post('/cards/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_cards(self):
        Card.objects.create(user=self.user, title='Test Card 1', censored_number='1234********5678', is_valid=True)
        Card.objects.create(user=self.user, title='Test Card 2', censored_number='5678********1234', is_valid=False)

        response = self.client.get('/cards/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        response = self.client.get('/cards/?title=Test Card 1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_card_validity_speed(self):
        import time
        import random

        random_card_data = [
            {'ccv': random.randint(100, 999), 'card_number': ''.join([str(random.randint(0, 9)) for _ in range(16)])}
            for _ in range(100)]

        start_time = time.time()

        for data in random_card_data:
            response = self.client.post('/cards/', data)

        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Time taken to create 100 cards: {execution_time} seconds")
        self.assertLess(execution_time, 5)

