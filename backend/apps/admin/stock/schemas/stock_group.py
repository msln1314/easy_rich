#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/02/08
# @File           : stock_group.py
# @IDE            : PyCharm
# @desc           : 股票分组 pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr
from datetime import datetime


class StockGroupCreate(BaseModel):
    """创建股票分组"""
    name: str = Field(..., description="分组名称", max_length=50)
    status: int = Field(1, description="是否禁用：0禁用 1启用")
    order: int | None = Field(None, description="显示排序")
    remark: str | None = Field(None, description="描述", max_length=255)
    parent_id: int | None = Field(None, description="上级分组ID")
    user_id: int | None = Field(None, description="用户ID")


class StockGroupUpdate(BaseModel):
    """更新股票分组"""
    name: str | None = Field(None, description="分组名称", max_length=50)
    status: int | None = Field(None, description="是否禁用：0禁用 1启用")
    order: int | None = Field(None, description="显示排序")
    remark: str | None = Field(None, description="描述", max_length=255)
    parent_id: int | None = Field(None, description="上级分组ID")


class StockGroupOut(BaseModel):
    """股票分组输出"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    status: int
    order: int | None = None
    remark: str | None = None
    parent_id: int | None = None
    user_id: int | None = None
    created_at: DatetimeStr
    updated_at: DatetimeStr


class StockGroupTreeOut(BaseModel):
    """股票分组树形输出"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    status: int
    order: int | None = None
    remark: str | None = None
    parent_id: int | None = None
    user_id: int | None = None
    children: list['StockGroupTreeOut'] = []
    created_at: DatetimeStr
    updated_at: DatetimeStr
