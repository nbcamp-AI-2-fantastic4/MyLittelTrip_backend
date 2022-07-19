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
    def delete(self, request):
        try:
            request_user = request.data.get("user", "")
            request_posttype = request.data.get("posttype", "")
            post_id = request.data.get("post_id", "")

            user = User.objects.get(id=request_user)
            posttype = PostType.objects.get(id=request_posttype)

            if not Like.objects.filter(user=user, posttype=posttype, post_id=post_id).exists():
                return Response({"error": "좋아요를 등록하지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)
            
            if Like.objects.filter(user=user, posttype=posttype, post_id=post_id).exists():
                Like.objects.filter(user=user, posttype=posttype, post_id=post_id).delete()
                return Response({"message": "좋아요 취소 성공"}, status=status.HTTP_200_OK)
        
        except:
            return Response({"error": "좋아요 취소 실패"}, status=status.HTTP_400_BAD_REQUEST)
