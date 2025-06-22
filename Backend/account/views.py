from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User, UserDetail
from .serializers import UserSignupSerializer, UserSerializer, UserDetailSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# 회원가입
class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = [AllowAny]

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

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': '회원가입이 완료되었습니다.',
            'user_id': user.user_id
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'detail': '아이디와 비밀번호를 입력해주세요.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user_id': user.user_id
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'detail': '아이디 또는 비밀번호가 올바르지 않습니다.'
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mypage(request):
    user = request.user
    return Response({
        'name': user.name,
        'user_id': user.user_id,
        'gender': user.gender,
        'birth_date': user.birth_date,
        'phone_number': user.phone_number,
        'address': user.address
    }, status=status.HTTP_200_OK)