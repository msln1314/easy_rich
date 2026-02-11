# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/24 16:44
# @File           : sms.py
# @IDE            : PyCharm
# @desc           : 主要接口文件

from fastapi import APIRouter, Depends, Body, UploadFile, Form, Request
from utils.response import SuccessResponse, ErrorResponse

from apps.admin.auth.utils.current import AllUserAuth, FullAdminAuth, OpenAuth,Auth
from .params import DeviceParams
from . import schemas, crud, models
from core.dependencies import IdList
from sqlalchemy.orm import joinedload
from datetime import datetime,timedelta


router = APIRouter()

###########################################################
#    设备管理
###########################################################
@router.post("", summary="创建设备")
async def create_device(data: schemas.Device, auth: Auth = Depends(AllUserAuth())):
    model = models.IotDevice
    options = [joinedload(model.product)]
    return SuccessResponse(await crud.DeviceDal(auth.db).create_data(data=data,v_options=options))


@router.get("", summary="获取设备列表，分页")
async def get_device(params: DeviceParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    model = models.IotDevice
    options = [joinedload(model.product)]
    device_dict = params.dict(exclude=[ 'online_status'])
    offline_time = datetime.now() - timedelta(minutes=5)
    v_where = []
    # v_join = [['product']]
    if params.online_status:
        print(params.online_status, "onlie")
        if params.online_status == "1":
            v_where.append(model.last_time >= offline_time)
        elif params.online_status == "0":
            v_where.append(models.IotDevice.last_time < offline_time)
        else:
            v_where.append(model.last_time.is_(None))
    datas, count = await crud.DeviceDal(auth.db).get_datas(**device_dict,v_where =v_where,v_options=options, v_return_count=True)
    for data in datas:
        last_time = data.get('last_time')
        if last_time:
            if datetime.strptime(last_time, "%Y-%m-%d %H:%M:%S") >= offline_time:
                data['online_status'] = 1
            else:
                data['online_status'] = 0
        else:
            data["online_status"] = -1
    print(datas,"datas")
    return SuccessResponse(datas, count=count)


@router.delete("", summary="批量删除设备", description="硬删除")
async def delete_device(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.DeviceDal(auth.db).delete_datas(ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@router.put("/{data_id}", summary="更新设备")
async def put_device(data_id: int, data: schemas.Device, auth: Auth = Depends(AllUserAuth())):

    return SuccessResponse(await crud.DeviceDal(auth.db).put_data(data_id, data))



@router.get("/options", summary="获取设备选择项")
async def get_device_options(params: DeviceParams = Depends(),auth: Auth = Depends(FullAdminAuth(permissions=["iot.client.create", "iot.client.update", "iot.client.bind"]))):
    device_dict = params.dict(exclude=['keywords'])
    # device_dict['ip'] ='12'
    model = models.IotDevice
    options = [joinedload(model.product)]
    v_where = []
    if params.keywords:
        v_where.append((models.IotDevice.mac.like('%'+params.keywords+'%')| models.IotDevice.ip.like('%'+params.keywords+'%')))
    datas = await crud.DeviceDal(auth.db).get_datas(**device_dict,v_where=v_where,v_options=options, v_return_count=False)
    return SuccessResponse(datas)


@router.get("/{data_id}", summary="获取设备详情")
async def get_device_detail(data_id: int, auth: Auth = Depends(AllUserAuth())):
    schema = schemas.DeviceSimpleOut
    model = models.IotDevice
    options = [joinedload(model.product)]
    return SuccessResponse(await crud.DeviceDal(auth.db).get_data(data_id, v_schema=schema,v_options= options))
