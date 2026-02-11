
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")
import time
import json, re
from pydantic import BaseModel
from apps.admin.iot.models.device import IotDevice
from application.settings import settings
import logging
import requests
import json,traceback
import base64
import asyncio
from sqlalchemy import func, delete, update, BinaryExpression, ScalarResult, select, false, insert
# 设置日志格式
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
print(__name__)
# 创建 logger 对象
logger = logging.getLogger(__name__)

from core.database import db_getter,session_factory




class EmQx:
    def __init__(self, ip='',port =18083):
        self.ip = ip
        self.port = port

        self.username = settings.MQTT_API_USERNAME#test
        # self.username = '334debcfbdc435a8'
        self.password = settings.MQTT_API_PASSWORD #test
        # self.password = 'YG1iZvhM6O79C029CospGYuZkKhEEWRqxOQtSDwEK1xAD'
        self.url = f'http://{self.ip}:{self.port}/api/v5/'
        self.auth_header = "Basic " + base64.b64encode((self.username + ":" + self.password).encode()).decode()
        self.headers = {'Content-Type': 'application/json;charset=UTF-8','Authorization':self.auth_header}
    def api_url_get(self, url,params={}):
        try:
            # if isinstance(payload, dict):
            #     payload.update(self.data)
            #     payload = parse.urlencode(payload).encode('utf-8')
            try:
                print(url,params)
                req = requests.get(url, verify=False,headers=self.headers,params=params
                                  )
            except:
                logging.warning(traceback.format_exc())
                req = None
            # print(req)
            # print(resp)
            return req
        except Exception as e:
            logging.warning(traceback.format_exc())
            return None
    def api_call_post(self, url, params):
        # print(url,params)
        try:
            req = requests.post(url, verify=False, json=params,headers=self.headers)
            # print(req)
            return req
        except Exception as e:
            logging.warning(traceback.format_exc())
            return None
    def api_call_put(self, url, params):
        try:
            req = requests.put(url, verify=False, json=params,headers=self.headers,auth =(self.user,self.password))
            return req
        except Exception as e:
            logging.warning(traceback.format_exc())
            return None
    def api_call_delete(self, url, params):
        try:
            print(url,params)
            req = requests.delete(url, verify=False, json=params,headers=self.headers,auth =(self.user,self.password))
            return req
        except Exception as e:
            logging.warning(traceback.format_exc())
            return None


    def get_nodes(self):
        url = self.url+'nodes'
        req = self.api_url_get(url)
        status,result =  self.parse_resp(req)
        return  status,result
    @staticmethod
    def total_page_num(count,limit):
        """
        计算最大的页码
        :return: 最大页码
        """

        if count % limit == 0:
            return count// limit
        else:
            return count// limit + 1

    def get_client(self,clientid):
        url = self.url + 'clients/'+clientid
        req = self.api_url_get(url)
        status, result = self.parse_resp(req)
        # print(result,"22")
        if status:
            print(result)

        # print(status,client_datas)
        return status,result
    def get_clients(self):
        client_datas = []
        url = self.url + 'clients'
        params ={"page":1,"limit":100}
        req = self.api_url_get(url,params)
        status, result = self.parse_resp(req)
        print(result,"22")
        if status:
            count = result.get('meta',{}).get('count',0)
            limit = result.get('meta',{}).get('limit',100)
            hasnext = result.get('meta', {}).get('hasnext')
            if not hasnext:
                client_datas.extend(result.get('data',[]))
            else:
                #进行分页
                # print("分页",hasnext,limit,count)
                page = self.total_page_num(count,limit)
                for i in range(1,page+1):
                    # print(i)
                    params = {"page": i, "limit": limit}
                    req = self.api_url_get(url,params)
                    status, result = self.parse_resp(req)
                    # print(result.get('data')[0].get('clientid'))
                    client_datas.extend(result.get('data',[]))

        # print(status,client_datas)
        return client_datas
    @staticmethod
    async def sync_clients( items):
        async with session_factory() as session:
            clients = await session.scalars(select(IotDevice).filter(IotDevice.is_delete==0))
            print(clients)
            client_macs = [i.mac for i in clients]
            for item in items:
                mac = item.get('mac')
                if mac in client_macs:
                    item.pop("mac")
                    await session.execute(update(IotDevice).where(IotDevice.mac == mac).values(**item))
                else:
                    await  session.execute(insert(IotDevice).values(**item))
            await session.commit()
    def parse_resp(self, req):
        status = True
        msg = None
        # print(req,"req",req.text)
        try:
            if req.content:
                print(1)
                resp = req.json()
                # print(resp,"23444445")
                if isinstance(resp,str):
                    resp = json.loads(req.json())
                    msg = resp
            else:
                print()
                status = False
            if isinstance(resp,dict):
                print(4,'NOT_FOUND' in resp.get('code',''))
                if 'NOT_FOUND' in resp.get('code',''):
                    print("4",resp)
                    status = False
                elif 'BAD' in resp.get('code',''):
                    status = False


                msg = resp

            elif isinstance(resp,list ):
                    msg = resp

            return status,msg
        except Exception as e:
            logging.warning(traceback.format_exc())
            return None,None




def main():
    # ip = '58.19.228.243'
    ip = MQTT_HOST
    print(ip)
    emqx = EmQx(ip)
    clients_data =emqx.get_clients()
    # c =  emqx.get_client('12351711366519351')
    # print(c,"cc")
    update_data =[]
    for i in clients_data:
        update_data.append({'ip':i['ip_address'],'port':i["port"],'connect_time':i['connected_at'],'keepalive':i['keepalive'],'mac':i['clientid']})

    asyncio.run( emqx.sync_clients(update_data))


if __name__ == '__main__':
    # 启动监听
    main()
