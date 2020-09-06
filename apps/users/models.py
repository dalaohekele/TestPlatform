from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    '''
    用户信息表
    '''
    name = models.CharField(max_length=32, null=False, blank=False, verbose_name="姓名")
    mobile = models.CharField(max_length=11, unique=True, null=False, blank=False, verbose_name="电话")
    email = models.EmailField(max_length=128, unique=True,null=False, blank=False, verbose_name="邮箱")
    # username 不做唯一处理
    username = models.CharField(max_length=30, unique=False)
    USERNAME_FIELD = 'mobile'


    class Meta:
        # 联合约束 mobile ,email不能重复
        unique_together = ["mobile", "email"]
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.name
