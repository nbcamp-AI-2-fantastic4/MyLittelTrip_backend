
from email.mime import image
import re
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from place.serializers import PlaceSerializer, PlaceTypeSerializer, PlaceAddSerializer, PlaceUpdateSerializer,PlaceDetailSerializer
from user.models import User
from place.models import Place, PlaceType, Duration
from faker import Faker
# Create your tests here.


# 이미지업로드

from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from PIL import Image
import tempfile


def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, 'png')
    return temp_file


class PlaceCreateTest(APITestCase):

    # def setUpTestData(cls):
    #     cls.user_data = {'email':'email@gmail.com','username': 'john', 'password': 'johnpassword'}
    #     cls.article_data = {'name':'경리단길','address':'210-65 Itaewon-dong, Yongsan-gu, Seoul','x':'126.9875° E','y':'37.5384° N','placetype':'여행장소','description':'경리단길이다','_id':'12345678','word':'경리단길'}
    #     cls.user = User.objects.create_user('email@gmail.com','john', 'johnpassword')

    # def setUp(self):
    # self.access_token = self.client.post(reverse('token'), self.user_data).data['access']
    # @classmethod
    def setUp(self):
        self.placetype_data = {"typename": "1"}
        self.placetype = PlaceType.objects.create(**self.placetype_data)
        self.user_data = {'email': 'email@gmail.com',
                          'username': 'john', 'password': 'johnpassword'}
        
        self.user = User.objects.create_user(
            'email@gmail.com', 'john', 'johnpassword')
        self.access_token = self.client.post(
            reverse('token'), self.user_data).data['access']
        self.place_data = {'name': '경리단길', 'address': '210-65 Itaewon-dong, Yongsan-gu, Seoul', 'x': '126.9875° E',
                           'y': '37.5384° N', 'placetype': '1', 'description': '경리단길이다', 'user': '1', '_id': '12345678', 'word': '경리단길'}
            
    def test_fail_if_not_logged_in(self):
        url = reverse("place_view")
        response = self.client.post(url, self.place_data)
        self.assertEqual(response.status_code, 401)

    # def test_create_article(self):
    #     response = self.client.post(path=reverse("place_view"),data=self.place_data, HTTP_AUTHORIZATION = f"Bearer {self.access_token}",format='json')
    #     # self.assertEqual(response.data["message"], "글 작성 완료!!")
    #     self.assertEqual(response.status_code, 200)

    # 장소 추가 
    def test_create_article_with_image(self):
        # 임시 이미지 파일 생성
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = "image.png"
        image_file = get_temporary_image(temp_file)
        image_file.seek(0)
        self.place_data["image"] = image_file

        #전송
        response = self.client.post(path=reverse("place_view"),data=encode_multipart(data=self.place_data, boundary=BOUNDARY),content_type=MULTIPART_CONTENT, HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        # self.assertEqual(response.data["message"],"글 작성 완료!!")
        self.assertEqual(response.status_code, 200)
    


# 장소 조회
class PlaceReadTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        
        cls.places =[]
        cls.placetype_data = {"typename": 1}
        cls.placetype = PlaceType.objects.create(**cls.placetype_data)
        cls.type_name = PlaceType.objects.get(id=1)
        for i in range(10):
            cls.user = User.objects.create_user(cls.faker.name(),cls.faker.word())
            # cls.placetype = PlaceType.objects.create(cls.faker.name())
            cls.places.append(Place.objects.create(name=cls.faker.sentence(), address=cls.faker.sentence(), x=cls.faker.sentence(),y=cls.faker.sentence(),placetype=cls.type_name,description=cls.faker.text(),_id=f'1234567{i}',word=cls.faker.word(), user=cls.user))


#  self.place_data = {'name': '경리단길', 'address': '210-65 Itaewon-dong, Yongsan-gu, Seoul', 'x': '126.9875° E',
#                            'y': '37.5384° N', 'placetype': '1', 'description': '경리단길이다', 'user': '1', '_id': '12345678', 'word': '경리단길'}

    #상세조회
    def test_get_place(self):
        for place in self.places:
            url = place.get_absolute_url()
            response = self.client.get(url)
            serializer = PlaceDetailSerializer(place).data
            for key, value in serializer.items():
                print(response.data)
                self.assertEqual(response.data[key],value)
        # self.assertEqual(place.title, response.data)
