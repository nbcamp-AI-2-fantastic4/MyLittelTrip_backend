from django.contrib.auth import authenticate
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


from .serializers import UserSerializer

# 유저 정보 기능
class UserInfoView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTAuthentication]
    
    # 유저 정보 조회
    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)
    
    # 회원가입
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)

        if user_serializer.is_valid():
            user_serializer.save()
            return Response({"message": "회원가입 성공"}, status=status.HTTP_200_OK)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 회원 정보 수정
    def put(self, request):
        user = request.user
        data = request.data

        # 현재 비밀번호를 잘못 입력했을 경우
        password = data.pop('password_current', '')
        user = authenticate(request, email=user.email, password=password)
        if not user:
            return Response({"error" : "비밀번호가 옳바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 수정
        user_serializer = UserSerializer(user, data=data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({"message": "회원정보 수정 성공"}, status=status.HTTP_200_OK)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 회원 탈퇴
    def delete(self, request):
        user = request.user
        data = request.data

        # 현재 비밀번호를 잘못 입력했을 경우
        password = data.get('password', '')
        user = authenticate(request, email=user.email, password=password)
        if not user:
            return Response({"error" : "비밀번호가 옳바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 회원 삭제
        user.delete()

        return Response({"message": "회원 삭제 성공"}, status=status.HTTP_200_OK)