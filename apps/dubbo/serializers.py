from rest_framework.serializers import ModelSerializer

from dubbo.models import DubboControllerLogs


class ControllerInfoSerializer(ModelSerializer):
    """
    接口详情序列化类
    """

    class Meta:
        model = DubboControllerLogs
        fields = '__all__'


class InvokeSerializer(ModelSerializer):
    class Meta:
        model = DubboControllerLogs
        fields = ("service_name", "dubbo_method", "params_type", "params")
