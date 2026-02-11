#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:19
# @File           : dict.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作
import datetime

from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr
from apps.admin.iot.models.client_group import IotClientGroup
# from apps.admin.iot.models.device import IotDevice
from .device import DeviceSimpleOut
from  .client_group import ClientGroupSimpleOut
class DevicePort(BaseModel):
    name: str
    status: int|None = 0
    device_id: int | None = None
    remark: str | None = None


class DevicePortSimpleOut(DevicePort):
    model_config = ConfigDict(from_attributes=True)
    id: int
    device: DeviceSimpleOut | None = None
    created_at: DatetimeStr
    updated_at: DatetimeStr

