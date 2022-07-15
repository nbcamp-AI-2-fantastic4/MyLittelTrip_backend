from rest_framework import serializers

from .models import (
    Trip as TripModel,
    TripCourse as TripCourseModel,
    TripCourseType as TripCourseTypeModel
)

class TripCourseSerializer(serializers.ModelSerializer):
    place = serializers.SerializerMethodField()
    tripcoursetype = serializers.SerializerMethodField()

    def get_place(self, obj):
        return obj.place.name

    def get_tripcoursetype(self, obj):
        return obj.tripcoursetype.typename

    class Meta:
        model = TripCourseModel
        fields = ["id", "trip", "place", "start_at", "end_at", "order", "tripcoursetype" ]

        read_only_fields = ("trip", )

# 여행일정 상세 조회를 위한 Serializer
class TripDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    tripcourse = TripCourseSerializer(many=True)

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = TripModel
        fields = ["id", "user", "title", "created_at", "content", "tripcourse"]

# 여행일정 리스트 조회를 위한 Serializer
class TripSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    tripcourse = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username
   
    def get_tripcourse(self, obj):
        tripcourse_all = obj.tripcourse.all()
        tripcourse = [ tripcourse.place.name for tripcourse in tripcourse_all]

        return tripcourse

    class Meta:
        model = TripModel
        fields = ["id", "user", "title", "created_at", "tripcourse"]