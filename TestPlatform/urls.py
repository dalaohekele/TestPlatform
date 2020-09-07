"""TestPlatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from users.views import UserRegisterView, UserViewset

router = DefaultRouter()
# 使用视图集，通过router.register 自动生成url
router.register(r'user/register', UserRegisterView, basename='register')

router.register(r'user',UserViewset,basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
    # 工具的Url
    path('api/utils/',include('utilsapp.urls')),
    #dubbo 的Url
    path('api/dubbo/',include('dubbo.urls')),

    path('api/user/login',obtain_jwt_token)
]
