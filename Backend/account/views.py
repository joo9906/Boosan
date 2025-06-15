from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import User, UserDetail
from .serializers import UserSignupSerializer, UserSerializer, UserDetailSerializer
from rest_framework import status

# 회원가입
class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

# 유저 정보 조회(GET), 수정(PUT/PATCH), 탈퇴(DELETE)
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # 인증된 사용자 본인만 접근 가능하도록
        return self.request.user

# 마이페이지 (GET만 지원)
class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 본인 UserDetail 생성 or 수정
class UserDetailUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # 본인의 userdetail이 없으면 새로 생성
        obj, created = UserDetail.objects.get_or_create(user=self.request.user)
        return obj