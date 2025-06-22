from django.urls import path
from . import views

urlpatterns = [
    path('hospitals/', views.hospital_list, name='hospital_list'),
    path('pill-upload/', views.pill_upload, name='pill_upload'),
    path('my-pills/', views.my_pills, name='my-pills'),
] 