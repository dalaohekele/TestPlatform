import configparser

import redis
from rest_framework import status
from rest_framework.exceptions import APIException, _get_error_details
from rest_framework.response import Response

from TestPlatform import settings


class PyRedis:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = '6379'
        self.db = 0
        pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db)
        self.conn = redis.Redis(connection_pool=pool)

    def set_key(self, key, value):
        try:
            return self.conn.set(name=key, value=str(value, encoding='gbk'))
        except Exception as e:
            print(e)

    def get_key(self, key):
        try:
            return self.conn.get(key)
        except Exception as e:
            print(e)

    def del_key(self, key):
        try:
            return self.conn.delete(key)
        except Exception as e:
            print(e)


class ReadConf:
    '''
    通用的读取配置文件的方法
    '''

    def __int__(self):
        pass

    def get_conf(self, section, option):
        conf_path = settings.CONF_DIR
        cf = configparser.ConfigParser()
        cf.read(conf_path)
        conf = cf.get(section, option)
        return conf


# 自定义状态码
class HttpCode(object):
    # 正常登陆
    ok = 200
    # 参数错误
    paramserror = 400
    # 权限错误
    unauth = 401
    # 方法错误
    methoderror = 405
    # 服务器内部错误
    servererror = 500


# 定义统一的 json 字符串返回格式
def result(code=HttpCode.ok, message="", data=None, kwargs=None):
    json_dict = {"code": code, "message": message, "data": data}
    # isinstance(object对象, 类型):判断是否数据xx类型
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)

    return Response(json_dict)


def ok():
    return result(message="success")


def ok_data(data=None):
    return result(data=data, message="success")


# 参数错误
def params_error(message="params error", data=None):
    return result(code=HttpCode.paramserror, message=message, data=data)


# 权限错误
def unauth(message="", data=None):
    return result(code=HttpCode.unauth, message=message, data=data)


# 方法错误
def method_error(message="methods error", data=None):
    return result(code=HttpCode.methoderror, message=message, data=data)


# 服务器内部错误
def server_error(message="server error", data=None):
    return result(code=HttpCode.servererror, message=message, data=data)


class OwnerValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid input'
    default_code = 'invalid'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        # For validation failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if not isinstance(detail, dict) and not isinstance(detail, list):
            detail = {detail}

        self.detail = _get_error_details(detail, code)
