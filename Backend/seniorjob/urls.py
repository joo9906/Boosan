from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# 필요한 ViewSet들을 여기에 등록

urlpatterns = [
    path('', include(router.urls)),
] 