from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from user.models import User

from comment.models import PostType, Like
from like.serializers import LikeSerializer

class LikeView(APIView):
    # 좋아요 등록 : /like/
    # 요청 헤더 : Authorization → user 임시 사용
    # 요청 바디 : post_id, posttype
    # 등록 성공 : 좋아요 등록 성공(message)
    # 중복 등록 : 이미 좋아요를 등록했습니다.(error)
    # 등록 실패 : 좋아요 등록 실패(error)
    def post(self, request):
        try:
            request_user = request.data.get("user", "")
            request_posttype = request.data.get("posttype", "")
            post_id = request.data.get("post_id", "")

            user = User.objects.get(id=request_user)
            posttype = PostType.objects.get(id=request_posttype)

            like_serializer = LikeSerializer(data=request.data)

            if Like.objects.filter(user=user, posttype=posttype, post_id=post_id).exists():
                return Response({"error": "이미 좋아요를 등록했습니다."}, status=status.HTTP_400_BAD_REQUEST)
            
            if like_serializer.is_valid():
                like_serializer.save(user=user, posttype=posttype)
                return Response({"message": "좋아요 등록 성공"}, status=status.HTTP_200_OK)
        
        except:
            return Response({"error": "좋아요 등록 실패"}, status=status.HTTP_400_BAD_REQUEST)

    # 좋아요 취소 : /like/
    # 요청 헤더 : Authorization → user 임시 사용
    # 요청 바디 : post_id, posttype
    # 등록 성공 : 좋아요 취소 성공(message)
    # 중복 등록 : 좋아요를 등록하지 않았습니다.(error)
    # 등록 실패 : 좋아요 취소 실패(error)
    def delete(self, request):
        return Response({})
