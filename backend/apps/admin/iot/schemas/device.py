#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/10/25 12:19
# @File           : dept.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作


from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr
from .product import DeviceProductSimpleOut


class Device(BaseModel):
    # name: str | None = None
    mac: str | None = None
    # status: bool = False
    device_tag: str | None = None
    device_type: str | None = None
    deal_status: int | None = None
    is_active: int | None = None
    remark: str | None = None
    address: str | None = None
    area: str | None = None
    deal_time: DatetimeStr | None = None
    check_time: DatetimeStr | None = None
    last_time: DatetimeStr | None = None
    ip: str | None = None
    phone: str | None = None
    ccid: str | None = None
    product_id: int | None = None


class ClientDeviceSimpleOut(Device):
    model_config = ConfigDict(from_attributes=True)
    # product: ProductSimpleOut

    id: int
    created_at: DatetimeStr


class DeviceSimpleOut(Device):
    model_config = ConfigDict(from_attributes=True)
    product: DeviceProductSimpleOut | None = None

    id: int
    created_at: DatetimeStr
