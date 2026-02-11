#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:19
# @File           : role.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作


from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr
from .menu import MenuSimpleOut
from .dept import DeptSimpleOut


class Role(BaseModel):
    name: str
    status: bool = False
    is_admin: bool | None = False
    order: int | None = None
    remark: str | None = None
    code: str


class RoleSimpleOut(Role):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: DatetimeStr
    updated_at: DatetimeStr


class RoleOut(RoleSimpleOut):
    model_config = ConfigDict(from_attributes=True)

    menus: list[MenuSimpleOut] = []



class RoleIn(Role):
    menu_ids: list[int] = []

class RoleOptionsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    label: str = Field(alias='name')
    value: int = Field(alias='id')
    status: bool

