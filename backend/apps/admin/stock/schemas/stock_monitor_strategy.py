#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version : 1.0
# @Create Time : 2025/02/15
# @File : stock_monitor_strategy.py
# @IDE : PyCharm
# @desc : 股票监听策略 pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr
from datetime import datetime


class StockMonitorStrategyCreate(BaseModel):
    """创建股票监听策略"""

    name: str = Field(..., description="监听策略名称", min_length=1, max_length=100)
    tag: str | None = Field(None, description="标签", max_length=50)
    user_id: int = Field(1, description="创建用户ID")
    stock_code: str | None = Field(
        None, description="监听股票代码，如000001", max_length=10
    )
    stock_name: str | None = Field(None, description="监听股票名称", max_length=50)
    strategy_type: str = Field(
        ...,
        description="监听策略类型：limit_up涨停/limit_down跌停/open_board开板/turnover换手/breakout突破/rebound反弹",
    )
    condition_content: str | None = Field(None, description="监听条件内容")
    trigger_value_min: float | None = Field(None, description="触发值最小值")
    trigger_value_max: float | None = Field(None, description="触发值最大值")
    trigger_percent_min: float | None = Field(None, description="触发百分比最小值")
    trigger_percent_max: float | None = Field(None, description="触发百分比最大值")
    cooldown_minutes: int = Field(60, description="冷却时间（分钟）", ge=0)
    cooldown_type: str = Field(
        "same_day",
        description="冷却类型：same_day同一天内只触发一次/interval按间隔时间触发",
    )
    is_active: int = Field(1, description="是否启用：1启用 0禁用")
    priority: int = Field(3, description="优先级：1高 2中 3低", ge=1, le=3)
    reason: str | None = Field(None, description="监听原因", max_length=255)
    remark: str | None = Field(None, description="备注")
    notify_enabled: int = Field(1, description="是否启用推送：1启用 0禁用")
    notify_method: str = Field(
        "system", description="推送方式：system系统消息/email邮件/sms短信/wechat微信"
    )
    notify_trigger_count: int = Field(
        1, description="推送触发条件：累计触发次数达到此值时才推送", ge=1
    )
    notify_type: str = Field(
        "once", description="推送类型：once仅一次/always每次都推送/interval按间隔推送"
    )
    strategy_config: str | None = Field(None, description="策略特定配置，JSON格式存储")


class StockMonitorStrategyUpdate(BaseModel):
    """更新股票监听策略"""

    name: str | None = Field(
        None, description="监听策略名称", min_length=1, max_length=100
    )
    tag: str | None = Field(None, description="标签", max_length=50)
    stock_code: str | None = Field(None, description="监听股票代码", max_length=10)
    stock_name: str | None = Field(None, description="监听股票名称", max_length=50)
    strategy_type: str | None = Field(None, description="监听策略类型")
    condition_content: str | None = Field(None, description="监听条件内容")
    trigger_value_min: float | None = Field(None, description="触发值最小值")
    trigger_value_max: float | None = Field(None, description="触发值最大值")
    trigger_percent_min: float | None = Field(None, description="触发百分比最小值")
    trigger_percent_max: float | None = Field(None, description="触发百分比最大值")
    cooldown_minutes: int | None = Field(None, description="冷却时间（分钟）", ge=0)
    cooldown_type: str | None = Field(None, description="冷却类型")
    is_active: int | None = Field(None, description="是否启用：1启用 0禁用")
    priority: int | None = Field(None, description="优先级：1高 2中 3低", ge=1, le=3)
    reason: str | None = Field(None, description="监听原因", max_length=255)
    remark: str | None = Field(None, description="备注")
    notify_enabled: int | None = Field(None, description="是否启用推送")
    notify_method: str | None = Field(None, description="推送方式")
    notify_trigger_count: int | None = Field(None, description="推送触发条件", ge=1)
    notify_type: str | None = Field(None, description="推送类型")
    strategy_config: str | None = Field(None, description="策略特定配置")


class StockMonitorStrategyOut(BaseModel):
    """股票监听策略输出"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    tag: str | None = None
    user_id: int
    stock_code: str | None = None
    stock_name: str | None = None
    strategy_type: str
    condition_content: str | None = None
    trigger_value_min: float | None = None
    trigger_value_max: float | None = None
    trigger_percent_min: float | None = None
    trigger_percent_max: float | None = None
    cooldown_minutes: int
    cooldown_type: str
    last_trigger_time: datetime | None = None
    last_trigger_count: int
    trigger_count: int
    is_active: int
    priority: int
    reason: str | None = None
    remark: str | None = None
    notify_enabled: int
    notify_method: str
    notify_trigger_count: int
    notify_type: str
    strategy_config: str | None = None
    created_at: DatetimeStr
    updated_at: DatetimeStr


class StockMonitorStrategyDetail(StockMonitorStrategyOut):
    """股票监听策略详情（含统计信息）"""

    pass


class StockMonitorStrategyStatistics(BaseModel):
    """策略统计信息"""

    total: int = Field(0, description="总策略数")
    active: int = Field(0, description="启用策略数")
    total_triggers: int = Field(0, description="总触发次数")
