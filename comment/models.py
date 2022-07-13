from turtle import ondrag
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from user.models import User

class PostType(models.Model):
    typename = models.CharField("게시글 유형", max_length=100, unique=True)

    def __str__(self):
        return self.typename

class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name="사용자", on_delete=models.CASCADE)
    posttype = models.ForeignKey(PostType, verbose_name="게시글 유형", on_delete=models.CASCADE)
    post_id = models.BigIntegerField("게시글", null=False)

    comment = models.TextField("댓글 내용")
    rating = models.FloatField("평점", validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    created_at = models.DateTimeField("작성일", auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} comments {self.posttype.typename}"

class Like(models.Model):
    user = models.ForeignKey(User, verbose_name="사용자", on_delete=models.CASCADE)
    posttype = models.ForeignKey(PostType, verbose_name="게시글 유형", on_delete=models.CASCADE)
    post_id = models.BigIntegerField("게시글", null=False)

    def __str__(self):
        return f"{self.user.username} likes {self.posttype.typename}"
