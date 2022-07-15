from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from review.models import Review, ReviewImage
from review.serializers import ReviewDetailSerializer, ReviewSerializer
from user.models import User


class ReviewView(APIView):

    # 리뷰 리스트 조회
    def get(self, request):
        reviews = Review.objects.all().order_by('-id')

        reviews_serializer = ReviewSerializer(reviews, many=True).data

        return Response(reviews_serializer, status=status.HTTP_200_OK)

    # 리뷰 작성하기
    def post(self, request):
        return Response({"msg":"post 요청"})


class ReviewDetailView(APIView):

    # 리뷰 상세보기
    def get(self, request, review_id):
        review_obj = Review.objects.all().get(id=review_id)
        
        review_obj_serializer = ReviewDetailSerializer(review_obj).data

        return Response(review_obj_serializer, status=status.HTTP_200_OK)
