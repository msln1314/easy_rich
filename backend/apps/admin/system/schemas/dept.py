#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/10/25 12:19
# @File           : dept.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作


from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr
from .menu import MenuSimpleOut


class Dept(BaseModel):
    name: str
    code: str
    status: bool = False
    order: int | None = None
    remark: str | None = None
    manager: str | None = None
    phone: str | None = None
    email: str | None = None

    parent_id: int | None = None


class DeptSimpleOut(Dept):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: DatetimeStr
    updated_at: DatetimeStr


class DeptTreeListOut(DeptSimpleOut):
    model_config = ConfigDict(from_attributes=True)

    children: list[dict] = []

