import re
import sys
import telnetlib
import time

from kazoo.client import KazooClient
from utilsapp.common import ReadConf


class TelnetClient(object):
    """通过telnet连接dubbo服务, 执行shell命令, 可用来调用dubbo接口
    """

    def __init__(self, server_host, server_port):
        self.tn = telnetlib.Telnet()
        self.server_host = server_host
        self.server_port = server_port

    # 此函数实现telnet登录主机
    def connect_dubbo(self):
        try:
            print("telent连接dubbo服务端: telnet {} {} ……".format(self.server_host, self.server_port))
            self.tn.open(self.server_host, port=self.server_port)
            return True
        except Exception as e:
            print('连接失败, 原因是: {}'.format(str(e)))
            return False

    # 此函数实现执行传过来的命令，并输出其执行结果
    def execute_some_command(self, command):
        # 执行命令
        cmd = (command + '\n').encode("gbk")
        self.tn.write(cmd)

        # 获取命令结果,字符串类型
        retry_count = 0
        # 如果响应未及时返回,则等待后重新读取，并记录重试次数
        result = self.tn.read_very_eager().decode(encoding='gbk')
        while result == '':
            time.sleep(1)
            result = self.tn.read_very_eager().decode(encoding='gbk')
            retry_count += 1
        return result

    def logout_host(self):
        self.tn.write(b"exit\n")
        print("登出成功")


class InvokeDubboApi(object):

    def __init__(self, server_host, server_port):
        try:
            self.telnet_client = TelnetClient(server_host, server_port)
            self.login_flag = self.telnet_client.connect_dubbo()
        except Exception as e:
            print("invokedubboapi init error" + str(e))

    def invoke_dubbo_api(self, dubbo_service, dubbor_method, *args):
        api_name = dubbo_service + "." + dubbor_method + "{}"
        cmd = "invoke " + api_name.format(args)
        print("调用命令是：{}".format(cmd))
        resp0 = None
        try:
            if self.login_flag:
                resp0 = self.telnet_client.execute_some_command(cmd)
                print("接口响应是,resp={}".format(resp0))
                # dubbo接口返回的数据中有 elapsed: 4 ms. 耗时，需要使用elapsed 进行切割
                return str(re.compile(".+").findall(resp0).pop(0)).split("elapsed").pop(0).strip()
            else:
                print("登陆失败！")
        except Exception as e:
            raise Exception("调用接口异常, 接口响应是resp={}, 异常信息为：{}".format(resp0, str(e)))
        self.logout()

    def logout(self):
        self.telnet_client.logout_host()


class GetDubboService(object):
    def __init__(self):
        self.hosts = ReadConf().get_conf("zookeeper_conf", "zookeeper_address")
        if self.hosts:
            self.hosts = self.hosts.split(',')
            self.zk = KazooClient(hosts=self.hosts)
            self.zk.start()  # 与zookeeper连接
        else:
            print("请配置zk地址信息zookeeper.address字段")
            sys.exit(0)

    def get_dubbo_info(self, dubbo_service):
        node = self.zk.get_children('/dubbo/' + dubbo_service + '/providers')
        from urllib import parse
        if node:
            server = parse.unquote(node[0])
            dubbore = re.compile(r"^dubbo://([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+:[0-9]+)", re.I)
            result = dubbore.match(server)
            if result:
                result = result.group(1)
                print("获取到dubbo部署信息" + result)
                return {"server_host": result.split(":")[0], "server_port": result.split(":")[1]}
        self.zk.stop()
