from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from user.models import User
from comment.models import PostType
from comment.models import Comment

# 댓글 조회 TestCode
class CommentGetAPIViewTest(APITestCase):
    # 테스트 더미 데이터
    def setUp(self):
        self.user_data = {"username": "admin", "email": "admin@email.com", "passowrd": "1234"}
        self.user = User.objects.create_user("admin", "1234")

        self.posttype_data = {"typename": "리뷰"}
        self.posttype = PostType.objects.create(**self.posttype_data)

        self.comment_data = {
            "user": 1,
            "posttype": 1,
            "post_id": 2,
            "comment": "댓글 테스트",
            "rating": 3.5
        }

    # 댓글 조회 테스트
    def test_comment_get(self):
        url = reverse("comment_get_view", kwargs={"posttype_id": 1, "post_id": 2})
        response = self.client.get(url)
        print("comment_get :", self.comment_data)
        self.assertEqual(response.status_code, 200)

# 댓글 작성 TestCode
class CommentPostAPIViewTest(APITestCase):
    # 테스트 더미 데이터
    def setUp(self):
        self.user_data = {"username": "admin", "email": "admin@email.com", "passowrd": "1234"}
        self.user = User.objects.create_user("admin", "1234")

        self.posttype_data = {"typename": "리뷰"}
        self.posttype = PostType.objects.create(**self.posttype_data)

        self.comment_data = {
            "user": 1,
            "posttype": 1,
            "post_id": 2,
            "comment": "댓글 테스트",
            "rating": 3.5
        }

    # 댓글 작성 성공 테스트
    def test_comment_post(self):
        response = self.client.post(
            path=reverse("comment_post_view"),
            data=self.comment_data,
            format="json",
        )
        print("comment_post :", response.data)
        self.assertEqual(response.status_code, 200)

    # 댓글 작성 실패 테스트
    def test_comment_post_fail(self):
        self.comment_data = {
            "user": 1,
            "posttype": 1,
            "post_id": None,
            "comment": "댓글 테스트",
            "rating": 3.5
        }

        response = self.client.post(
            path=reverse("comment_post_view"),
            data=self.comment_data,
            format="json",
        )
        print("comment_post_fail :", response.data)
        self.assertEqual(response.status_code, 400)

# 댓글 수정 TestCode
class CommentPutAPIViewTest(APITestCase):
    # 테스트 더미 데이터
    def setUp(self):
        self.user_data = {"username": "admin", "email": "admin@email.com", "passowrd": "1234"}
        self.user = User.objects.create_user("admin", "1234")

        self.posttype_data = {"typename": "리뷰"}
        self.posttype = PostType.objects.create(**self.posttype_data)

        self.comment = Comment.objects.create(
            user=self.user, posttype=self.posttype, post_id=2,
            comment="댓글 테스트", rating=3.5)

    # 댓글 수정 성공 테스트
    def test_comment_get(self):
        url = reverse("comment_put_delete_view", kwargs={"comment_id": 1})
        self.comment_put = {"user": 1, "comment": "수정", "rating": 2.2}
        response = self.client.put(
            path=url,
            data=self.comment_put,
            format="json",
        )
        print("comment_put :", response.data)
        self.assertEqual(response.status_code, 200)

    # 댓글 수정 실패 테스트
    def test_comment_put_fail(self):
        url = reverse("comment_put_delete_view", kwargs={"comment_id": 1})
        self.comment_put = {"user": 1, "comment": "수정", "rating": None}
        response = self.client.put(
            path=url,
            data=self.comment_put,
            format="json",
        )
        print("comment_put_fail :", response.data)
        self.assertEqual(response.status_code, 400)

# 댓글 삭제 TestCode
class CommentDeleteAPIViewTest(APITestCase):
    # 테스트 더미 데이터
    def setUp(self):
        self.user_data = {"username": "admin", "email": "admin@email.com", "passowrd": "1234"}
        self.user = User.objects.create_user("admin", "1234")

        self.posttype_data = {"typename": "리뷰"}
        self.posttype = PostType.objects.create(**self.posttype_data)

        self.comment = Comment.objects.create(
            user=self.user, posttype=self.posttype, post_id=2,
            comment="댓글 테스트", rating=3.5)

    # 댓글 삭제 성공 테스트
    def test_comment_delete(self):
        url = reverse("comment_put_delete_view", kwargs={"comment_id": 1})
        response = self.client.delete(url)
        print("comment_delete :", response.data)
        self.assertEqual(response.status_code, 200)

    # 댓글 삭제 실패 테스트
    def test_comment_delete_fail(self):
        url = reverse("comment_put_delete_view", kwargs={"comment_id": None})
        response = self.client.delete(url)
        print("comment_delete_fail :", response.data)
        self.assertEqual(response.status_code, 400)
