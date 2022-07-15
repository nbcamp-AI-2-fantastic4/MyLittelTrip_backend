from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from place.models import Place as PlaceModel
from .models import (
    Trip as TripModel,
    TripCourse as TripCourseModel,
    TripCourseType as TripCourseTypeModel,
    )
from .serializers import (
    TripSerializer, 
    TripDetailSerializer,
    TripCourseSerializer, 
    )

# 여행일정 기능
class TripView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTAuthentication]

    # 여행일정 리스트 조회
    def get(self, request):
        trip_all = TripModel.objects.all()
        return Response(TripSerializer(trip_all, many=True).data, status=status.HTTP_200_OK)

    # 여행일정 저장
    def post(self, request):
        # 여행일정 저장
        tripcourses = request.data.pop("tripcourse", "")

        trip_serializer = TripSerializer(data=request.data)
        if trip_serializer.is_valid():
            trip = trip_serializer.save(user=request.user)
        else:
            return Response({"error":"여행일정 정보가 옳바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 여행코스 저장
        for tripcourse in tripcourses:
            place_id = tripcourse.pop("place_id", "")
            try: 
                place = PlaceModel.objects.get(id=place_id)
            except:
                return Response({"error": "여행장소 정보가 옳바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

            tripcoursetype_id = tripcourse.pop("tripcoursetype_id", "")
            try:
                tripcoursetype = TripCourseTypeModel.objects.get(id=tripcoursetype_id)
            except:
                return Response({"error": "여행코스 유형 정보가 옳바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

            tripcourse_serializer = TripCourseSerializer(data=tripcourse)
            if tripcourse_serializer.is_valid():
                tripcourse_serializer.save(place=place, 
                                           tripcoursetype=tripcoursetype, 
                                           trip=trip)
            else:
                print(tripcourse_serializer.errors)
                return Response({"error": "여행코스 정보가 옳바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "저장 완료"}, status=status.HTTP_200_OK)

# 여행일정 상세 기능
class TripDetailView(APIView):
    permission_classes = [permissions.AllowAny]
    
    # 여행일정 상세 조회
    def get(self, request, trip_id):
        try :
            trip = TripModel.objects.get(id=trip_id)
        except:
            return Response({"error": "해당 여행일정이 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)


        return Response(TripDetailSerializer(trip).data, status=status.HTTP_200_OK)
    
