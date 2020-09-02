import configparser

import redis

from TestPlatform import settings


class PyRedis:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = '6379'
        self.db = 0
        pool = redis.ConnectionPool(host=self.host, port=self.port,db=self.db)
        self.conn = redis.Redis(connection_pool=pool)

    def set_key(self, key, value):
        try:
            return self.conn.set(name=key, value=str(value,encoding='gbk'))
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