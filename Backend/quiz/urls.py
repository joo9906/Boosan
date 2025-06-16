# quiz/urls.py

from django.urls import path
from . import views

app_name = 'quiz'
urlpatterns = [
    path('quiz/create/', views.create_quiz),
    path('quiz/<int:quiz_id>/submit/', views.submit_answer),
]
