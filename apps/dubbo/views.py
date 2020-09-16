import json

from django.core import serializers

# Create your views here.
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from dubbo.dubbo_client import GetDubboService, InvokeDubboApi
from dubbo.models import DubboControllerLogs
from dubbo.serializers import ControllerInfoSerializer, InvokeSerializer
from utilsapp.common import ok_data, params_error


class DubboApi(CreateAPIView):
    permission_classes = (IsAuthenticated,)  # 登陆才能请求
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = InvokeSerializer

    def post(self, request, *args):
        """
        请求Dubbo接口
        :param request:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user.id, params=json.dumps(request.data.get('params')))
        else:
            return params_error(message=serializer.errors)
        service_name = request.data.get('service_name')
        dubbo_method = request.data.get('dubbo_method')
        # 多参数类型，多参数
        params_type = request.data.get('params_type')
        params = request.data.get('params')
        dubbo_info = GetDubboService().get_dubbo_info(service_name)
        server_host = dubbo_info.get("server_host")
        server_port = dubbo_info.get("server_port")
        # 判断参数类型
        if params_type == "class":
            result = InvokeDubboApi(server_host, server_port).invoke_dubbo_api(service_name, dubbo_method, params)
        else:
            args = params
            result = InvokeDubboApi(server_host, server_port).invoke_dubbo_api(service_name, dubbo_method, *args)
        return ok_data(data=json.loads(result))


class DubboInfoView(RetrieveAPIView):
    serializer_class = ControllerInfoSerializer
    permission_classes = (IsAuthenticated,) # 登陆才能请求
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get(self, request, *args):
        id = request.GET.get('id')
        dubbo = DubboControllerLogs.objects.filter(id=id)
        dubbo_info_str = serializers.serialize('json', dubbo, fields=(
            "service_name", "dubbo_method", "params_type", "params", "user_id"))
        dubbo_info = json.loads(dubbo_info_str)
        return ok_data(data=dubbo_info[0].get("fields"))


class DubboPagination(PageNumberPagination):
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


class DubboInfosView(ListAPIView):
    serializer_class = ControllerInfoSerializer
    # 分页
    pagination_class = DubboPagination
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get(self, request, *args, **kwargs):
        service_name = request.GET.get("service_name")
        dubbo_method = request.GET.get("dubbo_method")
        if service_name =="" and dubbo_method =="":
            search_dubbo = DubboControllerLogs.objects.all()
            total = search_dubbo.count()
        elif service_name != "" and dubbo_method != "":
            search_dubbo = DubboControllerLogs.objects.filter(Q(service_name__icontains=service_name) &
                                                              Q(dubbo_method__icontains=dubbo_method))
            total = search_dubbo.count()
        elif dubbo_method != "":
            search_dubbo = DubboControllerLogs.objects.filter(Q(dubbo_method__icontains=dubbo_method))
            total = search_dubbo.count()
        else:
            search_dubbo = DubboControllerLogs.objects.filter(Q(service_name__icontains=service_name))
            total = search_dubbo.count()
        dubbo_infos_str = serializers.serialize('json', search_dubbo.order_by('-id'),
                                                fields=(
                                                    "service_name", "dubbo_method", "params_type", "params", "user_id"))
        dubbo_infos = json.loads(dubbo_infos_str)
        # 实例化分页对象，获取数据库中的分页数据
        paginator = DubboPagination()
        page_info_list = paginator.paginate_queryset(dubbo_infos, self.request, view=self)
        json_list = []
        for dubbo in page_info_list:
            dubbo_info = dubbo.get("fields")
            json_list.append(dubbo_info)
        return ok_data(data={"total": total, "dubbo_infos": json_list})