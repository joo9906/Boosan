from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# 필요한 ViewSet들을 여기에 등록

urlpatterns = [
    path('', include(router.urls)),
    # 건강 기록 및 AI 추천 관련 URL
    path('save-record/', views.save_health_record_and_recommend, name='save_health_record_and_recommend'),
    path('records/', views.get_health_records, name='get_health_records'),
    path('options/', views.health_recommendation_options, name='health_recommendation_options'),
    path('weekly-summary/', views.weekly_health_summary, name='weekly-health-summary'),
    path('recommendation/<str:date>/', views.get_recommendation, name='get-recommendation'),
] 