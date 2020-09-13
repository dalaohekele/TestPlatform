from django.urls import path

from apps.dubbo import views

urlpatterns = [
    path('invoke', views.DubboApi.as_view(), name='invoke'),
    path('info', views.DubboInfoView.as_view(), name='dubbo_info'),
    path('infos', views.DubboInfosView.as_view(), name='dubbo_info'),
]
