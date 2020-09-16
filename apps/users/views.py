import json

from django.core import serializers
from django.db.models import Q

# Create your views here.
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.backends import ModelBackend
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from users.models import User
from users.serializers import UserRegSerializer, UserDetailSerializer
from utilsapp.common import ok, params_error, unauth, ok_data, OwnerValidationError


class UserRegisterView(CreateAPIView):
    serializer_class = UserRegSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ok()
        else:
            return params_error(message=serializer.errors)


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(email=kwargs['mobile']) | Q(mobile=kwargs['mobile']))
            if user.check_password(password):
                return user
        except Exception as e:
            raise OwnerValidationError({"code": 400, "message": "用户名或密码错误", "data":""})


class UserInfoView(RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)  # 登陆才能请求
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get(self, request, *args):
        user_id = request.GET.get('id')
        if request.user.id != int(user_id):
            return unauth(message="无法查询他人信息")
        else:
            user = User.objects.filter(id=user_id)
            user_info_str = serializers.serialize('json', user, fields=("name", "email", "mobile"))
            user_info = json.loads(user_info_str)
            return ok_data(data=user_info[0].get("fields"))


class UsersPagination(PageNumberPagination):
    '''
    商品列表自定义分页
    '''
    # 默认每页显示的个数
    page_size = 10
    # 可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    # 页码参数
    page_query_param = 'page'
    # 最多能显示多少页
    max_page_size = 100


class UserInfosView(ListAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)  # 登陆才能请求
    # 分页
    pagination_class = UsersPagination
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get(self, request, *args, **kwargs):
        total = self.queryset.all().count()
        user_infos_str = serializers.serialize('json', self.queryset.all().order_by('-id'),
                                               fields=("name", "email", "mobile"))
        user_infos = json.loads(user_infos_str)
        # 实例化分页对象，获取数据库中的分页数据
        paginator = UsersPagination()
        page_user_list = paginator.paginate_queryset(user_infos, self.request, view=self)

        json_list = []
        for user in page_user_list:
            user_info = user.get("fields")
            json_list.append(user_info)
        return ok_data(data={"total": total, "users": json_list})
