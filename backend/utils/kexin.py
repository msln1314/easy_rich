import json,re
from pydantic import BaseModel
from utils.socket_client import SocketClient
#字符串
ip = '192.168.123.18'
port = 50000
data = '{"A01":110000, "A02":110000, "A03":110000, "A04": 110000, "A05": 110000, "res": "123"}'

data2 = '{"A01":100000,"A02":100000,"A03":100000,"A04":100000,"A05":100000,"res":"123"}'
class KeXinConfig(BaseModel):
    ip:str  =None
    mac:str =None
    port:int =50000
    platform:str



# {"ID":"CORX00021531","CCID":"898604F81623D1600198","A01":1,"B01":0,"res":"12345"}
# {"ID":"CORX00021531","CCID":"898604F81623D1600198","A01":1,"B01":0}
# {"ID":"CORX00021531","CCID":"898604F81623D1600198","A01":1,"B01":0,"res":"123"}
# {"ID":"CORX00021531","CCID":"898604F81623D1600198","A01":0,"B01":0,"res":"123"}

#
class Kexin:
    def __init__(self, config:KeXinConfig):
        # print(config.ip+config.platform)
        self.ip = config.ip
        self.mac = config.mac
        self.port = config.port
        self.platform = config.platform
        self.open = 110000
        self.close = 100000
    #生成命令行
    def generate_cmd(self, port_list, action):
        cmd = {}
        for port in port_list:
            cmd[port] = self.open if action else self.close
        cmd_str = json.dumps(cmd)
        cmd_str = cmd_str.replace(' ', '')
        return cmd_str

    def parse_response(self, port_list, action, response):
        result = {}
        status = True
        for port in port_list:
            print(port, response)
            if action != response[port]:
                status = False
            result[port] = response[port]

        return status, result

    def check_response(self, port_list, action, response):
        result = {}
        status = True
        for port in port_list:
            print(port, response)
            if action != response[port]:
                status = False
            result[port] = response[port]

        return status, result

    def generate_cmd(self,port_list,action):
        cmd = {}
        for port in port_list:
            cmd[port] = self.open if action else self.close
        cmd_str = json.dumps(cmd)
        cmd_str = cmd_str.replace(' ','')
        return cmd_str

    def send_string_to_tcp_server(self,ip,message,port=None):
        try:
            if port is None:
                port = self.port
            client = SocketClient(host=ip,port=port)
            client.tcp_send_message(message)

            response = client.client_socket.recv(1024).decode()
            print("从服务器接收到的响应：", response)
            client.close()
            result = re.search('({.*})',response)

            if result and result.group():
                print(result.group(1),"11")
                return json.loads(result.group(1))

            return None
        except Exception as e:
            raise Exception(f'错误信息:{str(e)}')

    def publish_string_to_mqtt_server(self, mqttclient,message, topic=None):
        try:
            if topic is None:
                topic = f'/set/{self.mac}'
            mqttclient.publish(topic, message)
            return None
        except Exception as e:
            raise Exception(f'错误信息:{str(e)}')


def main():
    # send_string_to_server(ip,port,new_data)
    b = KeXinConfig(port=port,ip=ip,platform='')
    a = Kexin(b)
    port_list = ['A01','A02','A03']
    action = False
    cmd_string = a.generate_cmd(port_list,action)
    # print(cmd_string)
    # cmd_string ='{"A01":0,"A02":0,"A03":0,"A04":0,"B01":0,"B02":0,"B03":0,"B04":0,"C01":0,"C02":0,"C03":0,"C04":0,"C05":0,"C06":0,"C07":0}'
    response = a.send_string_to_server(cmd_string)
    status,result = a.check_response(port_list,action,response)
    print('fan会',status,result)