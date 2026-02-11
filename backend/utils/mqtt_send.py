import paho.mqtt.client as mqtt

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# 参数有 Client(client_id="", clean_session=True, userdata=None, protocol=MQTTv311, transport="tcp")
client.connect("127.0.0.1", 1883, 60)  # 连接服务器,端口为1883,维持心跳为60秒
client.publish('test', 'test string2',1)
