#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:19
# @File           : dict.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作


from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr

class ProductCate(BaseModel):
    name: str
    remark: str | None = None
    order: int | None = None
    status: int | None = None


class ProductCateSimpleOut(ProductCate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: DatetimeStr
    updated_at: DatetimeStr
