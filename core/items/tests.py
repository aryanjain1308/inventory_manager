from django.urls import reverse
from rest_framework.test import APITestCase
from .models import Item
from django.contrib.auth.models import User
from rest_framework import status

class ItemCreateAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        response = self.client.post('/api/auth/login', {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.token = response.data['access']

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.create_url = reverse('item-list-create')

    def test_create_item(self):
        data = {
            "name": "Item1",
            "description": "description for item1",
            "price": 100.00
        }
        response = self.client.post(
            self.create_url, data, format='json'
        )

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(
            Item.objects.first().name, data['name']
        )

    def test_create_duplicate_item(self):
        Item.objects.create(
            name="Item1",
            description="description for item1",
            price=100.00
        )
        data = {
            "name": "Item1",
            "description": "description for duplicate item1",
            "price": 100.00
        }
        response = self.client.post(
            self.create_url, data, format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
            )

class ItemUpdateDeleteAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        response = self.client.post('/api/auth/login', {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.token = response.data['access']

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.item = Item.objects.create(
            name="Item1",
            description="description",
            price=100.00
        )
        self.update_url = reverse(
            'item-detail-update-delete',
            kwargs={'item_id':self.item.id}
        )

    def test_update_item(self):
        data = {
            "name": "Item1 update",
            "description": "description for item1 updated",
            "price": 200.00
        }
        response = self.client.put(
            self.update_url, data, format='json'
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data["name"], data["name"]
        )

    def test_delete_item(self):
        response = self.client.delete(self.update_url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(Item.objects.count(), 0)
