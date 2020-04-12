from django.urls import path
from compressor import views

urlpatterns = [
    path('compress/', views.compress),
]