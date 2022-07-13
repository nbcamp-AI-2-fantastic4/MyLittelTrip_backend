from django.db import models
from datetime import datetime
from place.models import Place as PlaceModel
from user.models import User as UserModel

class TripCourseType(models.Model):
    typename = models.CharField("유형", max_length=100)

    def __str__(self):
        return self.typename

class Trip(models.Model):
    user = models.ForeignKey(UserModel, verbose_name="사용자", on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=100)
    content = models.TextField("내용")
    created_at = models.DateTimeField("작성일", auto_now_add=True)
    start_at = models.DateTimeField("여행 시작일", null=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class TripCourse(models.Model):
    trip = models.ForeignKey(Trip, verbose_name="여행일정")
    tripcoursetype = models.ForeignKey(TripCourseType, verbose_name="여행 코스 유형", on_delete=models.CASCADE)
    place = models.ForeignKey(PlaceModel, verbose_name="여행 장소", on_delete=models.CASCADE)
    start_at = models.DateTimeField("시작 시간")
    end_at = models.DateTimeField("종료 시간")
    order = models.IntegerField("여행 코스 순서")

    def __str__(self):
        return f"{self.order} - {self.tripcoursetype} : {self.place.name}"


