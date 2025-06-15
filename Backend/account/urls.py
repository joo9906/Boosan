from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/', views.UserSignupView.as_view(), name='signup'),
    
    # 요거 하나로 조회, 수정, 탈퇴 다 할거임임
    path('profile/', views.UserDetailView.as_view(), name='profile'),

    # JWT 로그인
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('user/refresh/', TokenRefreshView.as_view(), name='userupdate'),
    
    # 마이페이지
    path('mypage/', views.UserMeView.as_view(), name='mypage'),
    # accounts/urls.py
    path('user/detail/', views.UserDetailUpdateView.as_view(), name='user-detail-update'),

]