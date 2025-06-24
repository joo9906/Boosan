from django.urls import path
from . import views

urlpatterns = [
    path('hospitals/', views.hospital_list, name='hospital-list'),
    path('pillupload/', views.upload_pill_image, name='upload_pill_image'),
    path('pills/', views.pill_list, name='pill_list'),
    path('quiz/create/', views.create_quiz, name='create_quiz'),
    path('quiz/<str:quiz_id>/submit/', views.submit_quiz_answer, name='submit_quiz_answer'),
] 