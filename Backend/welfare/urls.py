from django.urls import path
from . import views

urlpatterns = [
    path('centers/', views.welfare_center_list, name='welfare-center-list'),
] 