from django.apps import AppConfig
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from datetime import datetime, timedelta as t
import json

from recommend.functions import parsing, recommend, schedule


class ParsingView(APIView):
    def post(self, request):
        data = json.loads(request.body)
        place_type = data.get("type", '')
        place_word = data.get("word", '')

        if place_word == "":
            return Response({"message": "검색단어를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        place = parsing.parsing(place_type, place_word, [])
        return Response(place)


class ScheduleView(APIView):
    def post(self, request):
        data = json.loads(request.body)
        places = data.get("places", '')

        start_day = datetime(2022, 4, 14, 0, 0, 0)
        start_time = start_day + t(hours=10)
        add_place_index = [1, 1, 1, 1]

        # 여행 장소들의 정보를 담은 리스트
        places_info = []
        dists, route = recommend.dists_and_route(places, places_info)
        total_route, places_info = schedule.schedule(places, places_info, start_day, start_time, dists, route, add_place_index)

        result = {
            "result" : total_route,
            "places_info": places_info
        }

        return Response(result)