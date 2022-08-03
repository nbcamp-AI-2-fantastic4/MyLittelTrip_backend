from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User

class UserInfoViewTestCase(APITestCase):
    def test_registeration(self):
        url = reverse("user_info")
        user_data = { 
            "username": "dongwoo",
            "email": "test@email.com",
            "password": "0000",
            "fullname": "김동우"
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 200)


class LoginUserTest(APITestCase):
    def setUp(self):
        self.data = {
            "email": "admin@email.com",
            "username": "admin", 
            "password": "0000",
        }
        self.user = User.objects.create_user(**self.data)

    def test_login(self):
        response = self.client.post(reverse("token"), self.data)
        self.assertEqual(response.status_code, 200)

    def test_get_user_data(self):
        access_token = self.client.post(reverse("token"), self.data).data['access']
        response = self.client.get(
            path=reverse("user_info"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], self.data['username'])