from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class UserAuthTests(APITestCase):

    def test_user_registration(self):
        url = reverse('register')
        data = {
            "username": "testUser",
            "email": "testUser@test.com",
            "password": "test"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        url = reverse('token_obtain_pair')
        user = User.objects.create_user(
            username= "test_login",
            email= "test@test",
            password= "test_login"
            )
        data = {
            "username": "test_login",
            "password": "test_login"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_token(self):
        url = reverse('token_refresh')
        user = User.objects.create_user(
            username= "test1_login",
            email= "test1@test",
            password= "test_login"
        )
        refresh = RefreshToken.for_user(user)
        data = {
            "refresh": str(refresh)
        }
        response = self.client.post(url, data, form='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
