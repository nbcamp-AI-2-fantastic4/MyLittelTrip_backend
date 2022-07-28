from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from user.models import User
from comment.models import PostType
from comment.models import Like

# 좋아요 등록 TestCode
class LikePostAPIViewTest(APITestCase):
    # 테스트 더미 데이터
    def setUp(self):
        self.user_data = {"username": "admin", "email": "admin@email.com", "passowrd": "1234"}
        self.user = User.objects.create_user("admin", "1234")

        self.posttype_data = {"typename": "리뷰"}
        self.posttype = PostType.objects.create(**self.posttype_data)

        self.like_data = {"user": 1, "posttype": 1, "post_id": 2}

    # 좋아요 등록 성공 테스트
    def test_like_post(self):
        response = self.client.post(
            path=reverse("like_view"),
            data=self.like_data,
            format="json",
        )
        print("like_post :", response.data)
        self.assertEqual(response.status_code, 200)

    # 좋아요 등록 중복 에러 테스트
    def test_like_post_overlap(self):
        self.like = Like.objects.create(user=self.user, posttype=self.posttype, post_id=2)
        response = self.client.post(
            path=reverse("like_view"),
            data=self.like_data,
            format="json",
        )
        print("like_post_overlap :", response.data)
        self.assertEqual(response.status_code, 400)

    # 좋아요 등록 실패 테스트
    def test_like_post_fail(self):
        self.like_data = {"user": 1, "posttype": 1}
        response = self.client.post(
            path=reverse("like_view"),
            data=self.like_data,
            format="json",
        )
        print("like_post_fail :", response.data)
        self.assertEqual(response.status_code, 400)

# 좋아요 삭제 TestCode
class LikeDeleteAPIViewTest(APITestCase):
    # 테스트 더미 데이터
    def setUp(self):
        self.user_data = {"username": "admin", "email": "admin@email.com", "passowrd": "1234"}
        self.user = User.objects.create_user("admin", "1234")

        self.posttype_data = {"typename": "리뷰"}
        self.posttype = PostType.objects.create(**self.posttype_data)

        self.like = Like.objects.create(user=self.user, posttype=self.posttype, post_id=2)

        self.like_data = {"user": 1, "posttype": 1, "post_id": 2}

    # 좋아요 삭제 성공 테스트
    def test_like_delete(self):
        response = self.client.delete(
            path=reverse("like_view"),
            data=self.like_data,
            format="json",
        )
        print("like_delete :", response.data)
        self.assertEqual(response.status_code, 200)

    # 좋아요 삭제 미등록 에러 테스트
    def test_like_delete_not_register(self):
        self.like_data = {"user": 1, "posttype": 1, "post_id": 3}
        response = self.client.delete(
            path=reverse("like_view"),
            data=self.like_data,
            format="json",
        )
        print("like_delete_not_register :", response.data)
        self.assertEqual(response.status_code, 400)

    # 좋아요 삭제 실패 테스트
    def test_like_delete_fail(self):
        self.like_data = {"user": 1, "posttype": 1}
        response = self.client.delete(
            path=reverse("like_view"),
            data=self.like_data,
            format="json",
        )
        print("like_delete_fail :", response.data)
        self.assertEqual(response.status_code, 400)
