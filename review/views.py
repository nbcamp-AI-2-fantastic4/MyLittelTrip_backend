from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status,permissions
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


from review.models import Review, ReviewImage
from review.serializers import ReviewDetailSerializer, ReviewImageSerializer, ReviewSerializer
from user.models import User


# 리뷰 기능
class ReviewView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTAuthentication]

    # 리뷰 리스트 조회 : 로그인 안된 회원도 조회는 가능하게
    def get(self, request):
        reviews = Review.objects.all().order_by('-id')

        reviews_serializer = ReviewSerializer(reviews, many=True).data

        return Response(reviews_serializer, status=status.HTTP_200_OK)

        
    # 리뷰 작성하기 : 인증된 회원만
    def post(self, request):
        trip_id = request.data.pop('trip_id')[0]
        user_id = request.data.pop('user_id')[0]
        reviewimages = request.data.pop('image')
        
        # 리뷰 모델 저장
        review_serializer = ReviewSerializer(data=request.data)
        if review_serializer.is_valid():
            review = review_serializer.save(user_id=user_id, trip_id=trip_id)
        else:
            return Response(review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        # 이미지 모델 저장
        for index, reviewimage in enumerate(reviewimages):
            reviewimage_dict = {"image":reviewimage}

            reviewimage_serializer = ReviewImageSerializer(data=reviewimage_dict)
            if reviewimage_serializer.is_valid():
                reviewimage_serializer.save(review_id=review.id, order=index)
            else :
                return Response(reviewimage_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "저장 완료"}, status=status.HTTP_200_OK)


# 리뷰 상세 기능
class ReviewDetailView(APIView):

    # 리뷰 상세보기 : 로그인 안된 회원도 조회는 가능하게
    def get(self, request, review_id):
        try:
            review_obj = Review.objects.all().get(id=review_id)
        except:
            return Response({"error": "존재하지 않는 게시글 입니다."}, status=status.HTTP_400_BAD_REQUEST)

        review_obj_serializer = ReviewDetailSerializer(review_obj).data
        return Response(review_obj_serializer, status=status.HTTP_200_OK)
