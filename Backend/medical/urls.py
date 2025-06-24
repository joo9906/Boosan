from django.urls import path
from . import views

urlpatterns = [
    path('hospitals/', views.hospital_list, name='hospital_list'),
    path('pill-upload/', views.upload_pill_image, name='pill_upload'),
    path('my-pills/', views.pill_list, name='my-pills'),
] 