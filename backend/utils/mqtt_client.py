import sys
import os
import time
import paho.mqtt.client as mqtt
import json,re
from pydantic import BaseModel
import queue
import threading
import logging


# 设置日志格式
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
print(__name__)
# 创建 logger 对象
logger = logging.getLogger(__name__)

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")



class KeXinConfig(BaseModel):
    port:int =1883
    platform:str =None
    server:str = '58.19.228.243'
# {"ID":"CORX00021531","CCID":"898604F81623D1600198","A01":1,"B01":0,"res":"12345"}
# {"ID":"CORX00021531","CCID":"898604F81623D1600198","A01":1,"B01":0}
# {"ID":"CORX00021531","CCID":"898604F81623D1600198","A01":1,"B01":0,"res":"123"}
# {"ID":"CORX00021531","CCID":"898604F81623D1600198","A01":0,"B01":0,"res":"123"}
class KexinMqtt:
    def __init__(self, config:KeXinConfig):
        #print(config.ip+config.platform)
        # self.mac = config.mac
        self.port = config.port
        self.server = config.server
        self.platform = config.platform
        self.username = 'corxadmin'
        self.passwd = '1qaz@WSX'
        self.open = 110000
        self.close = 100000
        self.client= None
        self.message_queue = None
        self.client_connet()

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

    @staticmethod
    def on_connect(client, userdata, flags, rc, propertie):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}\n")
        REPORT_TOPIC = '/data/#'  # 主题
        client.subscribe(REPORT_TOPIC)  # 订阅主题
        print("订阅成功")

    @staticmethod
    def on_message(client,userdata, msg):
        print(userdata)
        message = msg.payload.decode()
        print(message,json.loads(message),msg)

    def client_connet(self):
        client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, transport='tcp', client_id=client_id)
        self.client = client
        self.client.connect(self.server, self.port, 60)  # 链接
        print(client)
        print("Connecting to")
        self.client.username_pw_set(self.username, password=self.passwd)
        print("成功")
        self.message_queue = queue.Queue()

    def process_message(self):
        print(12)
        while True:
            msg = self.message_queue.get()
            print("Processing message: ", msg)
            logging.info(msg)
            # # 存入数据库
            # cursor.execute("INSERT INTO messages (message) VALUES (?)", (msg,))
            # conn.commit()
            print("Message saved to database.")

            self.message_queue.task_done()
    def handle_message(self):
        print("开始新建队列")
        # 启动消息处理线程
        message_handler_thread = threading.Thread(target=self.process_message)
        message_handler_thread.daemon = True
        message_handler_thread.start()
        print("创建消息队列守护进程")

    def client_sub(self):

        self.client.on_connect = self.on_connect  # 启用订阅模式
        self.client.on_message = self.on_message  # 接收消息
        print(223)
        self.client.loop_start()   # 以start方式运行，需要启动一个守护线程，让服务端运行，否则会随主线程死亡
        # self.client.loop_forever()  # 以forever方式阻塞运行。

    def client_pub(self,mac,msg):
        topic = f'/set/{mac}' # 主题
        result = self.client.publish(topic, msg, 1)
        status = result[0]

        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")

        else:
            print(f"Failed to send message to topic {topic}")
        print(224)
        # client.loop_start()   # 以start方式运行，需要启动一个守护线程，让服务端运行，否则会随主线程死亡
        # self.client.loop_forever()  # 以forever方式阻塞运行。


    def server_stop(self):
        self.client.loop_stop()  # 停止服务端
        sys.exit(0)


def server_main():
    config = KeXinConfig()
    client = KexinMqtt(config)
    client.handle_message()
    client.client_sub()
    while True:
        pass






if __name__ == '__main__':
    # 启动监听
    server_main()
