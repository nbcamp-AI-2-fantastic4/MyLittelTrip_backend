from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from user.models import User

from comment.models import PostType, Like
from like.serializers import LikeSerializer

class LikeView(APIView):
    # 좋아요 등록 : /like/
    def post(self, request):
        return Response({})

    # 좋아요 취소 : /like/
    def delete(self, request):
        return Response({})
