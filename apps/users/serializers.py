from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


class UserRegSerializer(serializers.ModelSerializer):
    name = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False)
    mobile = serializers.CharField(label="手机号", help_text="手机号", required=True, allow_blank=False,
                                   validators=[UniqueValidator(queryset=User.objects.all(), message="手机号已经存在")])
    email = serializers.EmailField(label="邮箱号", help_text="邮箱号", required=True, allow_blank=False,
                                   validators=[UniqueValidator(queryset=User.objects.all(), message="邮箱号已经存在")])
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )


    class Meta:
        model = User
        fields = ("name", "mobile", "email", 'password')
