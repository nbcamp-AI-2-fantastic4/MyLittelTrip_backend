from django.apps import AppConfig
from django.shortcuts import render

# Create your views here.
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from recommend.functions import parsing


class ParsingView(APIView):
    def post(self, request):
        place_type = request.data.get("type", '')
        place_word = request.data.get("word", '')

        if place_word == "":
            return Response({"message": "검색단어를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        place = parsing.parsing(place_type, place_word, [])
        return Response(place)


class DurationView(APIView):
    def post(self, request):
        request.data["places_info"] = []
        duration = parsing.duration_minute(**request.data)
        
        return Response(duration)