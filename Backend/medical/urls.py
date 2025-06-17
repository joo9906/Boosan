from django.urls import path
from . import views

urlpatterns = [
    path('hospitals/', views.hospital_list, name='hospital-list'),
    path('pillupload/', views.upload_pill_image, name='upload_pill_image'),
    path('pills/', views.pill_list, name='pill_list')
] 