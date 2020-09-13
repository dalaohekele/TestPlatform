from django.db import models

# Create your models here.
from django.db.models import Model


class DubboControllerLogs(Model):
    service_name = models.CharField(max_length=128, unique=False, null=False, blank=False, verbose_name="服务名")
    dubbo_method = models.CharField(max_length=64, unique=False, null=False, blank=False, verbose_name="方法名")
    params_type = models.CharField(max_length=16, null=True, blank=True, verbose_name="参数类型")
    params = models.CharField(max_length=2048,default="", verbose_name="参数")
    user_id = models.IntegerField(verbose_name="请求人的ID")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")  # auto_now_add 设置为True,添加时间不可变
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")  # auto_now 设置为True,更新时间可变

    class Meta:
        db_table = "dubbo_controller_logs"
        verbose_name = "Dubbo接口请求记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.service_name + "#" + self.dubbo_method
