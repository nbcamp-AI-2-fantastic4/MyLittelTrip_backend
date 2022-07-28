from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from review.serializers import ReviewDetailSerializer, ReviewSerializer

from .models import Review, ReviewImage
from user.models import User
from trip.models import Trip

# 이미지 업로드에 필요한 라이브러리
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from PIL import Image
import tempfile

from faker import Faker

# 이미지파일 생성 함수
def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, 'png')
    return temp_file

# 리뷰 작성 테스트
class ReviewCreateTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # 임시 이미지 파일 생성
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = 'static/images/review/20220721/Red_Rock.png'
        image_file = get_temporary_image(temp_file)
        image_file.seek(0)  

        cls.user_data = {
            'username': 'minki', 
            'password': 'qwer1234', 
            'fullname': 'choiminki', 
            'email': 'minki@minki.com'
            }

        cls.review_data = {
            'user_id': 1,
            'title': 'test1',
            'content': 'test1 content,test1 content,test1 content,test1 content',
            'image': image_file,
            'trip_id': 1
            }

        cls.user = User.objects.create_user('minki@minki.com', 'minki', 'qwer1234')
        
        Trip.objects.create(user_id=1)

    # .client 는 cls.client 로 사용할 수 없음.
    def setUp(self):
        self.access_token = self.client.post(reverse('token'), self.user_data).data['access']


    # 토큰 없이 리뷰 작성 테스트
    def test_fail_if_not_logged_in(self):
        url = reverse('review_view')
        response = self.client.post(url, self.review_data)
        self.assertEqual(response.status_code, 401)
        # self.assertTrue(status.is_success(response.status_code))


    # 리뷰 작성 테스트
    def test_create_review_with_image(self):
                
        response = self.client.post(
            path=reverse('review_view'),
            data=encode_multipart(data=self.review_data, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            # format='json'
        )
        # self.assertEqual(response.data['message'], '저장 완료')
        self.assertEqual(response.status_code, 200)


    # 토큰 없이 리뷰 수정 테스트
    def test_update_fail_if_not_logged_in(self):
        url = reverse('review_detail_view', kwargs={'review_id':1})
        response = self.client.put(url, self.review_data)
        self.assertEqual(response.status_code, 401)
        # self.assertTrue(status.is_success(response.status_code))


    # 토큰 없이 리뷰 삭제 테스트
    def test_delete_fail_if_not_logged_in(self):
        url = reverse('review_detail_view', kwargs={'review_id':1})
        response = self.client.delete(url, self.review_data)
        self.assertEqual(response.status_code, 401)
        # self.assertTrue(status.is_success(response.status_code))        


# 리뷰 조회 테스트
class ReviewDetailReadTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        Trip.objects.create(user_id=1)

        # 리뷰모델 더미 데이터 생성
        cls.faker = Faker()
        cls.reviews = []
        cls.reviewimages = []
        for i in range(10):
            cls.user = User.objects.create_user(f'minki{i}@minki.com', cls.faker.name(), cls.faker.word())
            cls.reviews.append(Review.objects.create(
                user_id= cls.user.id,
                title= cls.faker.sentence(),
                content= cls.faker.text(),
                # images= v,
                trip_id= 1,
            ))
            cls.reviewimages.append(ReviewImage.objects.create(
                review_id= i+1,
                order= i,
                image= f'static/images/review/20220721/Red_Rock{i}.png'
            ))


    # 전체 리뷰 조회 테스트
    def test_get_review(self):
        url = reverse('review_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    # 상세 리뷰 조회 테스트
    def test_get_review_detail(self):
        url = reverse("review_detail_view", kwargs={"review_id": 1})
        response = self.client.get(url)

        review = Review.objects.get(id=1)
        review_serializer = ReviewDetailSerializer(review).data    # response와 비교

        self.assertEqual(review_serializer['user'], response.data['user'])
        self.assertEqual(review.title, response.data['title'])


