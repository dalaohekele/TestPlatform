def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {"code": 200, "message": "登录成功", "data": {"token": token}}