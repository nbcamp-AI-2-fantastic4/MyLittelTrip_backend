from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from place.serializers import PlaceSerializer, PlaceAddSerializer, PlaceUpdateSerializer,PlaceDetailSerializer
from .models import Place, PlaceType
from user.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.
# 장소 상세 조회
class PlaceViewDetail(APIView):
    def get(self,request,place_id):
        detailplaces = Place.objects.get(id=place_id)
        return Response(PlaceDetailSerializer(detailplaces).data, status=status.HTTP_200_OK)


class PlaceViewAll(APIView):
    authentication_classes = [JWTAuthentication] #JWT 인증
    # 장소 모두 조회
    def get(self, request):
        allplaces = Place.objects.all()
        return Response(PlaceSerializer(allplaces, many=True).data, status=status.HTTP_200_OK)

    

    # 장소 등록
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"message": "로그인해주세요"}, status=status.HTTP_401_UNAUTHORIZED)

        request.data['rating'] = 0
        image = request.FILES.get("image", "")
        placetype_typename = request.data.pop('placetype', '')[0]
        placetype_object = PlaceType.objects.get(typename=placetype_typename)
        user_id = request.data.pop('user', '')[0]
        user_object = User.objects.get(id=user_id)

        placeadd_serializer = PlaceAddSerializer(data=request.data)
  
        if placeadd_serializer.is_valid():
            placeadd_serializer.save(user=user_object,placetype=placetype_object,image=image)
            return Response(placeadd_serializer.data, status=status.HTTP_200_OK)
        return Response(placeadd_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 장소 수정

    def put(self, request, place_id):

            place = Place.objects.get(id=place_id)

            place_serializer = PlaceUpdateSerializer(place,data=request.data,partial=True)

            if place_serializer.is_valid():
                place_serializer.save()
                return Response({"message": "정상"}, status=status.HTTP_200_OK)
        
            return Response(place_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    #장소 삭제

    def delete(self, request, place_id):
        place = Place.objects.get(id=place_id)
        place.delete()
        return Response({"msg":"삭제완료"})        
                
           