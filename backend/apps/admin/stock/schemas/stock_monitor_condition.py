#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/28
# @File           : stock_monitor_condition.py
# @IDE            : PyCharm
# @desc           : 股票监控配置 pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr


class StockMonitorConditionCreate(BaseModel):
    """创建股票监控配置"""
    condition_content: str = Field(..., description="股票代码")
    tag: str | None = Field(None, description="股票名称")
    name: str = Field(..., description="监控名称/描述")
    user_id: int = Field(1, description="创建用户ID")
    is_active: int = Field(1, description="是否启用：1启用 0禁用")
    remark: str | None = Field(None, description="备注")
    owner: str | None = Field(None, description="拥有者")
    reason: str | None = Field(None, description="条件原因")
    watch_days: int | None = Field(None, description="关注7天")


class StockMonitorConditionUpdate(BaseModel):
    """更新股票监控配置"""
    condition_content: str | None = Field(None, description="股票代码")
    tag: str | None = Field(None, description="股票名称")
    name: str | None = Field(None, description="监控名称/描述")
    user_id: int | None = Field(None, description="创建用户ID")
    is_active: int | None = Field(None, description="是否启用：1启用 0禁用")
    remark: str | None = Field(None, description="备注")
    owner: str | None = Field(None, description="拥有者")
    reason: str | None = Field(None, description="条件原因")
    watch_days: int | None = Field(None, description="关注7天")


class StockMonitorConditionOut(BaseModel):
    """股票监控配置输出"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    condition_content: str
    tag: str | None = None
    name: str
    user_id: int
    is_active: int
    remark: str | None = None
    owner: str | None = None
    reason: str | None = None
    watch_days: int | None = None
    created_at: DatetimeStr
    updated_at: DatetimeStr
