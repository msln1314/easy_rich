#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/02/08
# @File           : sys_user_stock_group.py
# @IDE            : PyCharm
# @desc           : 用户股票分组关联 pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr


class SysUserStockGroupCreate(BaseModel):
    """创建用户股票分组关联"""
    user_id: int = Field(..., description="用户ID")
    group_id: int = Field(..., description="分组ID")
    stock_id: int | None = Field(None, description="股票ID")


class SysUserStockGroupUpdate(BaseModel):
    """更新用户股票分组关联"""
    user_id: int | None = Field(None, description="用户ID")
    group_id: int | None = Field(None, description="分组ID")
    stock_id: int | None = Field(None, description="股票ID")


class SysUserStockGroupOut(BaseModel):
    """用户股票分组关联输出"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int | None = None
    group_id: int | None = None
    stock_id: int | None = None
    created_at: DatetimeStr
    updated_at: DatetimeStr


class MyStockOut(BaseModel):
    """我的自选股输出"""
    id: int
    stock_code: str
    stock_name: str | None = None
    current_price: float | None = None
    change_percent: float | None = None
    change_amount: float | None = None
    volume: float | None = None
    amount: float | None = None
    high_price: float | None = None
    low_price: float | None = None
    open_price: float | None = None
    close_price: float | None = None
    pe_ratio: float | None = None
    pb_ratio: float | None = None
    total_market_cap: float | None = None
    circulating_market_cap: float | None = None
    turnover_rate: float | None = None
    volume_ratio: float | None = None
    follow_price: float | None = None
    follow_change_percent: float | None = None
    follow_remark: str | None = None
    group_id: int | None = None
    group_name: str | None = None
    created_at: DatetimeStr
