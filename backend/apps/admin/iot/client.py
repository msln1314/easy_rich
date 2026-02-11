# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/24 16:44
# @File           : sms.py
# @IDE            : PyCharm
# @desc           : 主要接口文件
import logging

from fastapi import APIRouter, Depends, Body, UploadFile, Form, Request,FastAPI
from utils.response import SuccessResponse, ErrorResponse
from datetime import  datetime,timedelta
from apps.admin.auth.utils.current import AllUserAuth, FullAdminAuth, OpenAuth,Auth
from apps.admin.system.crud import UserDal
from .params import ClientParams
from . import schemas, crud, models
from apps.admin.log.schemas.action import ActionLog
from core.dependencies import IdList
from core.exception import CustomException
from sqlalchemy.orm import joinedload
from utils.kexin import Kexin,KeXinConfig
from utils.emqx import EmQx
from apps.admin.log.models import SysActionLog
from apps.admin.system.models import SysUser
from apps.admin.system.schemas import UserOut

from application.settings import settings
# from core.database import mqtt_getter
router = APIRouter()




###########################################################
#    客户端管理
###########################################################

# @router.get("/test")
# async def func():
#     print(fast_mqtt)
#     fast_mqtt.publish("/data", "Hello from Fastapi")  # publishing mqtt topic
#     return {"result": True, "message": "Published"}


@router.post("", summary="创建客户端")
async def create_client(data: schemas.Client, auth: Auth = Depends(AllUserAuth())):
    options = [joinedload(models.IotClient.device), joinedload(models.IotClient.group)]
    client = await crud.ClientDal(auth.db).create_data(data=data,v_options=options)
    auth.db.commit()
    return SuccessResponse(client)


@router.get("", summary="获取单个客户端下的客户端列表，分页")
async def get_client(params: ClientParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    print('parammmmmmmmmmmmmmmmmmmmm',params.dict())

    options = [joinedload(SysUser.roles), joinedload(SysUser.iot_groups), joinedload(SysUser.dept)]
    schema = UserOut

    user = await UserDal(auth.db).get_data(auth.user.id, v_options=options, v_schema=schema)
    print(user)
    model = models.IotClient
    options = [joinedload(model.device),joinedload(model.group)]
    v_join = [ ['device']]

    client_dict = params.dict(exclude=['name','keywords','online_status','group_id','port_status'])

    # device_dict['ip'] ='12'

    offline_time = datetime.now()-timedelta(minutes=5)
    v_where = []
    # print("where",v_where)
    if not auth.user.is_super():
        user_groups = [i['id'] for i in user.get('iot_groups',[])]
        v_where.append(model.group_id.in_(user_groups))
    if params.group_id:

        child_ids = await crud.ClientGroupDal(auth.db).get_child_ids(params.group_id)
        print("idss",child_ids)
        v_where.append(model.group_id.in_(child_ids))
    if params.keywords:
        v_where.append((models.IotDevice.mac.like('%'+params.keywords+'%')| models.IotDevice.ip.like('%'+params.keywords+'%')))
    if params.port_status is not None:
        if params.port_status == 1:
            v_where.append((model.port_status ==1) & (model.connect_model =='常开')|((model.port_status ==0) & (model.connect_model =='常闭')))
        elif params.port_status == 0:
            v_where.append((model.port_status == 1) & (model.connect_model == '常闭') | (
                        model.port_status == 0) & (model.connect_model == '常开'))
        else:
            v_where.append(model.port_status == params.port_status)

    # print(device_where)
    if params.name:
        v_where.append((models.IotClient.sn.like('%' + params.name + '%') | models.IotClient.name.like(
            '%' + params.name + '%')))
    if params.online_status:
        print(params.online_status,"onlie")
        if params.online_status == "1":
            v_where.append(models.IotDevice.last_time >=offline_time)
        elif params.online_status == "0":
            v_where.append(models.IotDevice.last_time <offline_time)
        else:
            v_where.append(model.device_id.is_(None))
    datas, count = await crud.ClientDal(auth.db).get_datas(**client_dict,v_outer_join=v_join,v_options=options,v_where=v_where, v_return_count=True)

    for data in datas:
        #判断常闭的情况下做个转化

        if data.get('connect_model') == '常闭' and data['port_status'] in [0,1]:
            # print("ssssssssssssss")
            data['port_status'] = 0 if  data['port_status'] == 1 else 1



        device = data.get('device',{})
        if device:
            last_time = device.get('last_time')
            # print(last_time,type(last_time))
            if last_time :
                if datetime.strptime(last_time,"%Y-%m-%d %H:%M:%S") >= offline_time:
                    data['online_status'] = 1
                else:
                    data['online_status'] = 0
            else:
                data["online_status"] = -1

        else:
            data["online_status"] = -1
    # ids = [i['device_id'] for i in datas]
    # port_options = [joinedload(models.IotDevicePort.device)]
    # print(port_options,ids)
    # port_data = await crud.DevicePortDal(auth.db).get_datas(v_options=port_options,v_where=[models.IotDevicePort.device_id.in_(ids)])
    # print(port_data)
    # port_dict ={}
    # for i in port_data:
    #     if i['device_id'] in port_dict:
    #         port_dict[i['device_id']][i['name']] = i['status']
    #     else:
    #         port_dict[i['device_id']] = {i['name']:i['status']}
    # for item in datas:
    #     item['port_status'] = port_dict.get(item['device_id'],{}).get(item['port'])
    return SuccessResponse(datas, count=count)


@router.post("/export/excel", summary="导出用户查询列表为excel")
async def export_query_list(
        header: list = Body(..., title="表头与对应字段"),
        params: ClientParams = Depends(),
        auth: Auth = Depends(FullAdminAuth(permissions=["iot.client.export"]))
):
    options = [joinedload(SysUser.roles), joinedload(SysUser.iot_groups), joinedload(SysUser.dept)]
    schema = UserOut

    user = await UserDal(auth.db).get_data(auth.user.id, v_options=options, v_schema=schema)
    print(user)
    model = models.IotClient
    options = [joinedload(model.device), joinedload(model.group)]
    v_join = [['device']]
    params.limit = 1000000
    client_dict = params.dict(exclude=['name', 'keywords', 'online_status', 'group_id', 'port_status'])

    # device_dict['ip'] ='12'

    offline_time = datetime.now() - timedelta(minutes=5)
    v_where = []
    # print("where",v_where)
    if not auth.user.is_super():
        user_groups = [i['id'] for i in user.get('iot_groups', [])]
        v_where.append(model.group_id.in_(user_groups))
    if params.group_id:
        child_ids = await crud.ClientGroupDal(auth.db).get_child_ids(params.group_id)
        print("idss", child_ids)
        v_where.append(model.group_id.in_(child_ids))
    if params.keywords:
        v_where.append((models.IotDevice.mac.like('%' + params.keywords + '%') | models.IotDevice.ip.like(
            '%' + params.keywords + '%')))
    if params.port_status is not None:
        if params.port_status == 1:
            v_where.append((model.port_status == 1) & (model.connect_model == '常开') | (
                        (model.port_status == 0) & (model.connect_model == '常闭')))
        elif params.port_status == 0:
            v_where.append((model.port_status == 1) & (model.connect_model == '常闭') | (
                    model.port_status == 0) & (model.connect_model == '常开'))
        else:
            v_where.append(model.port_status == params.port_status)

    # print(device_where)
    if params.name:
        v_where.append((models.IotClient.sn.like('%' + params.name + '%') | models.IotClient.name.like(
            '%' + params.name + '%')))
    if params.online_status:
        print(params.online_status, "onlie")
        if params.online_status == "1":
            v_where.append(models.IotDevice.last_time >= offline_time)
        elif params.online_status == "0":
            v_where.append(models.IotDevice.last_time < offline_time)
        else:
            v_where.append(model.device_id.is_(None))
    datas = await crud.ClientDal(auth.db).get_datas(**client_dict, v_outer_join=v_join, v_options=options,
                                                           v_where=v_where, v_return_count=False)

    return SuccessResponse(await crud.ClientDal(auth.db).export_xlsx(header, datas))


@router.delete("", summary="批量删除客户端", description="硬删除")
async def delete_client(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.ClientDal(auth.db).delete_datas(ids.ids, v_soft=False)
    return SuccessResponse("删除成功")
#执行通断
@router.put("/status/{data_id}", summary="更新客户端端口状态")
async def put_status_client(request: Request,data_id: int, data: schemas.ClientPortStatus, auth: Auth = Depends(AllUserAuth())):
    schema = schemas.ClientSimpleOut
    model = models.IotClient

    options = [joinedload(model.device), joinedload(model.group)]
    client = await crud.ClientDal(auth.db).get_data(data_id,v_options=options)
    run_status_text = '断开'
    if client.connect_model == '常闭':
        data.port_status = 1 if data.port_status == 0 else 0
        if data.port_status == 0:
            run_status_text = '合闸'
    else:
        if data.port_status == 1:
            run_status_text = '合闸'
            # print("cllentkkk",client)
    if not client.port or client.device is None:
        raise CustomException("无法执行存在客户端关联的设备,未绑定端口", code=400,status_code=400)
    # product = await crud.P(auth)
    platform = ''
    if client.connect_protocol == 'tcp':
        if client.device.ip is None:
            raise CustomException("无法执行存在客户端关联的设备,没有ip地址", code=400,status_code=400)
        kexin_config = KeXinConfig(platform=platform)
        kexin = Kexin(kexin_config)
        port_list = [client.port]
        try:
            action = True if client.port_status ==1 else False
            cmd_string = kexin.generate_cmd(port_list, action)
            response = kexin.send_string_to_server(client.device.ip,cmd_string)
            status, result = kexin.check_response(port_list, action, response)
        except Exception as e:
            print(str(e))
            # log = ActionLog(device_id=client.device_id, client_id=client.id, phone=auth.user.phone,message=str(e),user_id =auth.user.id)
            # await SysActionLog.create_action_log(auth.db, log.dict(), False, request)
            raise CustomException(f"执行异常:{e}",code=400)
    elif client.connect_protocol == 'mqtt':
        if client.device.mac is None:
            raise CustomException("无法执行存在充电桩关联的设备,没有mac地址", code=400,status_code=400)
        emqx = EmQx(MQTT_HOST)
        online, result = emqx.get_client(client.device.mac)
        print(online,result,"online")
        if not online:
            raise CustomException(f"关联设备{client.device.mac} 不在线，操作失败", code=400,status_code=400)
        kexin_config = KeXinConfig(mac=client.device.mac, platform=platform)
        kexin = Kexin(kexin_config)
        port_list = [client.port]

        try:
            action = True if data.port_status == 1 else False
            cmd_string = kexin.generate_cmd(port_list, action)
            response = kexin.publish_string_to_mqtt_server(fast_mqtt,cmd_string)
            print("response",response,cmd_string,"执行下发命令")
            log = ActionLog(device_id=client.device_id, client_id=client.id, phone=auth.user.phone, message=f'执行{client.sn}  {client.name}: {client.port} {client.connect_model} {run_status_text}  调用命令{cmd_string}成功',
                            user_id=auth.user.id,status =1)
            print(log)
            await SysActionLog.create_action_log(auth.db, log.dict(), request)
            # status, result = kexin.check_response(port_list, action, response)
        except Exception as e:
            print("错误",str(e))
            log = ActionLog(device_id=client.device_id, client_id=client.id, phone=auth.user.phone, message=f'执行{client.sn}  {client.name}: {client.port} {client.connect_model} {run_status_text} 调用命令 {cmd_string} 失败，错误信息{str(e)}',
                            user_id=auth.user.id,status = 0)
            await SysActionLog.create_action_log(auth.db, log.dict(), request)
            raise CustomException(f"执行异常:{e}", code=400)
    # print('fan会', status, result)
    else:
        raise CustomException(f"不支持连接协议{client.connect_protocol}", code=400, status_code=400)
    client = await crud.ClientDal(auth.db).put_data(data_id, data)
    print(client)
    # auth.db.commit()
    return SuccessResponse(client)

@router.put("/{data_id}", summary="更新客户端")
async def put_client(data_id: int, data: schemas.ClientUpdate, auth: Auth = Depends(AllUserAuth())):
    client = await crud.ClientDal(auth.db).put_data(data_id, data)
    auth.db.commit()
    return SuccessResponse(client)


@router.put("/bind/{data_id}", summary="绑定客户端")
async def put_bind_client(data_id: int, data: schemas.ClientBind, auth: Auth = Depends(AllUserAuth())):

    client = await crud.ClientDal(auth.db).update_bind_info(data_id,data)
    auth.db.commit()
    return SuccessResponse(client)
@router.put("/unbind/{data_id}", summary="解除绑定客户端")
async def put_unbind_client(data_id: int, auth: Auth = Depends(AllUserAuth())):

    return SuccessResponse(await crud.ClientDal(auth.db).update_unbind_info(data_id))

@router.get("/{data_id}", summary="获取客户端详情")
async def get_client_detail(data_id: int, auth: Auth = Depends(AllUserAuth())):
    schema = schemas.ClientSimpleOut
    model = models.IotClient
    options = [joinedload(model.device),joinedload(model.group)]
    data = await crud.ClientDal(auth.db).get_data(data_id,v_options=options, v_schema=schema)
    # ids = [data['device_id']]
    # port_options = [joinedload(models.IotDevicePort.device)]
    # print(port_options,ids)
    # port_data = await crud.DevicePortDal(auth.db).get_datas(v_options=port_options,v_where=[models.IotDevicePort.device_id.in_(ids)])
    # print(port_data)
    # port_dict ={}
    # for i in port_data:
    #     if i['device_id'] in port_dict:
    #         port_dict[i['device_id']][i['name']] = i['status']
    #     else:
    #         port_dict[i['device_id']] = {i['name']:i['status']}
    #
    # data['port_status'] = port_dict.get(data['device_id'],{}).get(data['port'])


    return SuccessResponse(data)


