from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('hospitals/', views.hospital_list, name='hospital-list'),
    path('pillupload/', views.upload_pill_image, name='upload_pill_image'),
    path('pills/', views.pill_list, name='pill_list'),
    path('quiz/create/', views.create_quiz, name='create_quiz'),
    path('quiz/<str:quiz_id>/submit/', views.submit_quiz_answer, name='submit_quiz_answer'),
=======
    path('hospitals/', views.hospital_list, name='hospital_list'),
    path('pill-upload/', views.pill_upload, name='pill_upload'),
    path('my-pills/', views.my_pills, name='my-pills'),
>>>>>>> 40721384858c1ae68b7564ded00217523903aa00
] 