from django.urls import path

from apps.utilsapp import views

urlpatterns = [
    path('redis', views.redis_value, name='redis'),
]
