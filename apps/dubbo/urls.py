from django.urls import path

from apps.dubbo import views

urlpatterns = [
    path('invoke', views.DubboApi.as_view(), name='invoke'),
]
