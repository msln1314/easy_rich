#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:19
# @File           : dict.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作
# import datetime

from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr
from apps.admin.iot.models.client_group import IotClientGroup
# from apps.admin.iot.models.device import IotDevice
from .device import ClientDeviceSimpleOut
from .client_group import ClientGroupSimpleOut

from datetime import datetime
class Client(BaseModel):
    name: str
    sn: str
    area : str
    address : str |None = None
    client_type : str | None = None
    client_tag : str | None = None
    group_id : int | None = None
    device_id: int | None = None
    remark: str | None = None
    connect_type: str | None = None
    port: str | None = None
    connect_protocol: str | None = None
    port_status: int | None = None
    is_active: int | None = None




class ClientPortStatus(BaseModel):
    id : int | None = None
    port_status: int | None = None
    updated_at: DatetimeStr | None = datetime.now()


class ClientIn(Client):

    """
    创建客户端
    """
    ip: str | None = ""

class ClientUpdate(Client):
    remark:str | None = None


    # deal_status: int | None = None
    # connect_type:str | None = None
    # sn: str | None = None

class ClientBind(Client):
    # remark:str | None = None
    port: str | None = None
    bind_status: int | None = None
    connect_model : str | None = None
    bind_time: datetime|None = datetime.now()
    # deal_status: int | None = None
    # connect_type:str | None = None
    # sn: str | None = None
class ClientUnBind(BaseModel):

    # remark:str | None = None
    port: str | None = None
    port_status: int  = -1
    bind_status: int | None = None
    bind_time: datetime|None = None
    connect_model: str | None = None
    device_id : int | None = None

class ClientSimpleOut(Client):
    model_config = ConfigDict(from_attributes=True)

    id: int
    deal_status: int | None = None
    # remark: str | None = None
    bind_status: int
    connect_model: str | None = None
    bind_time: DatetimeStr|None = None
    deal_time: DatetimeStr | None = None
    is_active : int | None = False
    device: ClientDeviceSimpleOut | None = None
    group: ClientGroupSimpleOut|None = None
    created_at: DatetimeStr
    updated_at: DatetimeStr

