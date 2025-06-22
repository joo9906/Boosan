# quiz/urls.py

from django.urls import path
from . import views

app_name = 'quiz'
urlpatterns = [
    # 새로운 퀴즈 시스템 API
    path('daily/', views.get_daily_quiz, name='get_daily_quiz'),
    path('submit/', views.submit_quiz_answer, name='submit_quiz_answer'),
    path('statistics/', views.get_quiz_statistics, name='get_quiz_statistics'),
    path('category/<str:category>/', views.get_quiz_by_category, name='get_quiz_by_category'),
]
