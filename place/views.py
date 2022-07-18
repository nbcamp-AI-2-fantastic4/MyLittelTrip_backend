from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from place.serializers import PlaceSerializer
from .models import Place, PlaceType
# Create your views here.


class PlaceViewAll(APIView):

    # 장소 모두 조회
    def get(self, request):
        allplaces = Place.objects.all()
        print(allplaces)
        return Response( PlaceSerializer(allplaces, many=True).data, status=status.HTTP_200_OK)

    # 장소 등록
    def post(self, request):
        # request.data['user']
        print(request.data)
        request.data['rating']=0
        image = request.FILES.get("image", "")
        place_serializer = PlaceSerializer(data=request.data)
        print(place_serializer)
        if place_serializer.is_valid():
            place_serializer.save(user=request.user, typename=request.typename, image=image)
            return Response(place_serializer.data, status=status.HTTP_200_OK)
        return Response(place_serializer.errors, status=status.HTTP_400_BAD_REQUEST)