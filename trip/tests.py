from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from user.models import User as UserModel


class TripCreateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "email": "admin@email.com",
            "username": "admin",
            "password": "0000",
        }
        cls.user = UserModel.objects.create_user(**cls.user_data)
        cls.trip_data = {
                            "title" : "여행일정 저장용 1번",
                            "content" : "여행일정 저장용 1번입니다.",
                        }

    def setUp(self):
        self.access_token = self.client.post(reverse("token"), self.user_data).data["access"]

    def test_fail_if_not_logged_in(self):
        url = reverse("trip")
        response = self.client.post(url, self.trip_data)
        self.assertEqual(response.status_code, 400)