from turtle import ondrag
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class PostType(models.Model):
    typename = models.CharField("게시글 유형", max_length=50)

    def __str__(self):
        return self.typename

class Comment(models.Model):
    user = models.ForeignKey("user.User", verbose_name="사용자", on_delete=models.CASCADE)
    post = models.ForeignKey("review.Review", verbose_name="게시글", on_delete=models.CASCADE)
    typename = models.ForeignKey(PostType, verbose_name="게시글 유형", on_delete=models.CASCADE)
    comment = models.CharField("댓글 내용", max_length=100)
    rating = models.FloatField("평점", validators=[MinValueValidator(0.1), MaxValueValidator(5.0)])
    created_at = models.DateTimeField("작성일", auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}님이 '{self.post.title}'게시글에 작성한 댓글입니다."

class Like(models.Model):
    user = models.ForeignKey("user.User", verbose_name="사용자", on_delete=models.CASCADE)
    post = models.ForeignKey("review.Review", verbose_name="게시글", on_delete=models.CASCADE)
    typename = models.ForeignKey(PostType, verbose_name="게시글 유형", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}님이 '{self.post.title}'게시글에 좋아요를 눌렀습니다."
