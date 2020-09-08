from django.urls import path

from users import views

urlpatterns = [
    path('register', views.UserRegisterView.as_view(), name='register'),

    path('info',views.UserInfoView.as_view(),name='user_info'),

    path('info_list',views.UserInfosView.as_view(),name='user_info_list')
]
