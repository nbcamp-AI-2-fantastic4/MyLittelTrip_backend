from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from user.models import User

# 장소 타입 모델
class PlaceType(models.Model):
    typename = models.CharField("장소 유형", max_length=100, unique=True)

    def __str__(self):
        return self.typename

# 장소 모델
class Place(models.Model):
    _id = models.BigIntegerField("장소 id", unique=True)
    user = models.ForeignKey(User, verbose_name="등록자", on_delete=models.CASCADE)
    placetype = models.ForeignKey(PlaceType, verbose_name="장소 유형", on_delete=models.CASCADE)
    
    name = models.CharField("장소 이름", max_length=100)
    word = models.CharField("검색단어",  max_length=100)
    address = models.CharField("주소",  max_length=100)
    
    x = models.CharField("x좌표(경도)", max_length=50)
    y = models.CharField("y좌표(위도)", max_length=50)

    image = models.ImageField('장소 이미지', upload_to="static/images/place/%Y%m%d", null=True)
    rating = models.FloatField("평점", validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], default=0.0)
    description = models.TextField("설명", null=True)

    def __str__(self):
        return self.name


# 이동시간 모델
class Duration(models.Model):
    start_id = models.BigIntegerField("출발지 장소 id")
    start_place = models.ForeignKey(Place, verbose_name="출발지", on_delete=models.CASCADE, related_name="start_place")
    end_id = models.BigIntegerField("도착지 장소 id")    
    end_place = models.ForeignKey(Place, verbose_name="도착지", on_delete=models.CASCADE, related_name="end_place")
    duration = models.IntegerField("이동시간")
    
    def __str__(self):
        return f"{self.start_place.name} - {self.end_place.name} : {self.duration}"
