from operator import mod
from django.db import models

# Create your models here.

# 기간 모델
class Duration(models.Model):
    duration = models.IntegerField("이동시간")
    
    def __str__(self):
        return self.duration


# 장소 타입 모델
class PlaceType(models.Model):
    typename = models.CharField(max_length=100)

    def __str__(self):
        return self.typename

# 장소 모델
class Place(models.Model):

    typename = models.ForeignKey(PlaceType, verbose_name="타입", on_delete=models.CASCADE)
    name = models.CharField(max_length=100,unique=True)
    word = models.CharField("검색단어",  max_length=100)
    address = models.CharField("주소",  max_length=100)
    x = models.CharField("x좌표(경도)", max_length=50)
    y = models.CharField("y좌표(위도)", max_length=50)
    image = models.ImageField('신발 이미지', upload_to="static/")
    rating = models.FloatField("평점",max_length=10)
    description = models.TextField("설명")
    def __str__(self):
        return self.name



