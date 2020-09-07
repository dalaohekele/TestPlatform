from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth.backends import ModelBackend
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from users.models import User
from users.serializers import UserRegSerializer, UserDetailSerializer


class UserRegisterView(CreateModelMixin, GenericViewSet):
    serializer_class = UserRegSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(email=kwargs['mobile']) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class UserViewset(RetrieveModelMixin,GenericViewSet):
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_serializer_class(self):
        if self.action =='retrieve':
            return UserDetailSerializer
        elif self.action =='create':
            return UserRegSerializer

    def get_permissions(self):
        '''
        动态获取 permission权限
        :return:
        '''
        if self.action =='retrieve':

            return [permissions.IsAuthenticated()]
        elif self.action =='create':
            return []
        return []

