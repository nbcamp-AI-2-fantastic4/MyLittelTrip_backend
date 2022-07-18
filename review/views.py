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

    def put(self, request, review_id):
        
        # 리뷰 모델 수정
        try:
            review = Review.objects.get(id=review_id)
        except:
            return Response({"error": "존재하지 않는 게시글 입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        review_serializer = ReviewSerializer(review, data=request.data, partial=True)

        if review_serializer.is_valid():
            review_serializer.save()
        else:
            return Response(review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 이미지 모델 수정 
        # if 'image' in request.data:
        #     image = request.data.pop('image')
        #     order = request.data['order']

        #     review_images = ReviewImage.objects.filter(review=review_id)
        #     try:
        #         review_image = review_images.get(order=order)
        #     except:
        #             return Response({"error": "이미지 모델이 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
            
        #     reviewimage_dict = {"image":image}
        #     review_image_serializer = ReviewImageSerializer(review_image, data=reviewimage_dict, partial=True)
        #     if review_image_serializer.is_valid():
        #         review_image_serializer.save()
        #     else:
        #         return Response(review_image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # for index, image in enumerate(images):
            #     reviewimage_dict = {"image":image}
            #     review_image_serializer = ReviewImageSerializer(review_image, data=reviewimage_dict, partial=True)

            #     if review_image_serializer.is_valid():
            #         review_image_serializer.save()
            #     else:
            #         return Response(review_image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        return Response({"message":"수정 완료!"})

    def delete(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
        except:
            return Response({"error": "존재하지 않는 게시글 입니다."}, status=status.HTTP_400_BAD_REQUEST)
        review.delete()
        return Response({"message":"삭제 완료!"})
