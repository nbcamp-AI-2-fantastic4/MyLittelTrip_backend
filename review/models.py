from distutils.command.upload import upload
from django.db import models

from user.models import User
from trip.models import Trip

# 리뷰 모델
class Review(models.Model):
    user = models.ForeignKey(User, verbose_name='작성자', on_delete=models.SET_NULL, null=True)
    trip = models.ForeignKey(Trip, verbose_name='여행 일정', on_delete=models.SET_NULL, null=True)
    title = models.CharField('제목', max_length=50)
    content = models.TextField('내용')
    created_at = models.DateTimeField('등록일', auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s review - {self.id}"

# 리뷰 이미지 모델
class ReviewImage(models.Model):
    review = models.ForeignKey(Review, verbose_name='리뷰', on_delete=models.CASCADE)
    image = models.ImageField('이미지', upload_to='static/images/')
    order = models.IntegerField()

    def __str__(self):
        return f"{self.review.id}'s image - {self.order}"