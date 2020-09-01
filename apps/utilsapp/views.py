from rest_framework.decorators import api_view
from rest_framework.response import Response

from .common import PyRedis


# Create your views here.

@api_view(['GET', 'POST', 'DELETE'])
def redis_value(request):
    if request.method == 'GET':
        value = PyRedis().get_key(request.GET.get('redis_key'))
        res_data = {'redis_value': str(value)}
        return Response(res_data)

    elif request.method == 'POST':
        value = PyRedis().set_key(request.data.get('redis_key'), request.data.get('redis_value'))
        res_data = {'success': value}
        return Response(res_data)
    elif request.method == 'DELETE':
        value = PyRedis().del_key(request.data.get('redis_key'))
        res_data = {'success': value}
        return Response(res_data)
