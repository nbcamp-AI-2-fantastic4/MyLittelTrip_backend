from django.contrib import admin
from .models import Trip, TripCourse, TripCourseType

admin.site.register(Trip)
admin.site.register(TripCourse)
admin.site.register(TripCourseType)