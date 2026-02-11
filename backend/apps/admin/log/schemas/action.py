#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:19
# @File           : operation.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作


from pydantic import BaseModel, ConfigDict
from core.data_types import DatetimeStr
from apps.admin.iot.schemas.device import ClientDeviceSimpleOut
from apps.admin.system.schemas.user import UserSimpleOut
class ActionLog(BaseModel):
    phone: str | None = None
    user_id: int | None = None
    client_id:  int | None = None
    device_id:  int | None = None
    status: int | None = None
    message: str
    device:ClientDeviceSimpleOut|None = None
    user: UserSimpleOut | None = None



class ActionLogSimpleOut(ActionLog):
    model_config = ConfigDict(from_attributes=True)

    created_at: DatetimeStr
