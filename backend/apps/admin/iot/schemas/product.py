#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:19
# @File           : dict.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作


from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr
# from apps.admin.iot.models.client_group import IotClientGroup
# from apps.admin.iot.models.device import IotDevice
from .product_cate import ProductCateSimpleOut


class Product(BaseModel):
    name: str
    remark: str | None = None
    product_tag: str | None = None
    cate_id: int | None = None


class ProductSimpleOut(Product):
    model_config = ConfigDict(from_attributes=True)
    cate: ProductCateSimpleOut | None = None
    id: int
    created_at: DatetimeStr
    updated_at: DatetimeStr

class DeviceProductSimpleOut(Product):
    model_config = ConfigDict(from_attributes=True)
    # cate: ProductCateSimpleOut | None = None
    id: int
    created_at: DatetimeStr
    updated_at: DatetimeStr

class ProductOptionsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    label: str = Field(alias='name')
    value: int = Field(alias='id')
    status: bool | None = None
