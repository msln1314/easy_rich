#!/usr/bin python
# -*- coding: utf-8 -*-
# @version : 1.0
# @Create Time : 2025/02/15
# @File : stock_monitor_log.py
# @IDE : PyCharm
# @desc : 股票监听推送日志 pydantic 模型

from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr
from datetime import datetime


class StockMonitorLogCreate(BaseModel):
    """创建股票监听日志"""

    strategy_id: int = Field(..., description="监听策略ID")
    strategy_name: str = Field(..., description="监听策略名称", max_length=100)
    user_id: int = Field(..., description="用户ID")
    stock_code: str = Field(..., description="股票代码", max_length=10)
    stock_name: str | None = Field(None, description="股票名称", max_length=50)
    strategy_type: str = Field(..., description="监听策略类型")
    trigger_time: datetime | None = Field(None, description="触发时间")
    trigger_count: int = Field(0, description="触发时累计次数")
    trigger_condition: str | None = Field(None, description="触发条件描述")
    trigger_value: float | None = Field(None, description="触发时的数值")
    trigger_percent: float | None = Field(None, description="触发时的百分比")
    price: float | None = Field(None, description="触发时股票价格")
    change_percent: float | None = Field(None, description="触发时涨跌幅")
    volume: int | None = Field(None, description="触发时成交量")
    turnover_rate: float | None = Field(None, description="触发时换手率")
    notify_status: int = Field(0, description="推送状态")
    notify_time: datetime | None = Field(None, description="推送时间")
    notify_method: str | None = Field(None, description="推送方式")
    notify_content: str | None = Field(None, description="推送内容")
    notify_result: str | None = Field(None, description="推送结果")
    error_message: str | None = Field(None, description="错误信息")
    strategy_config_snapshot: str | None = Field(None, description="策略配置快照")
    remark: str | None = Field(None, description="备注")


class StockMonitorLogUpdate(BaseModel):
    """更新股票监听日志"""

    notify_status: int | None = Field(None, description="推送状态")
    notify_time: datetime | None = Field(None, description="推送时间")
    notify_result: str | None = Field(None, description="推送结果")
    error_message: str | None = Field(None, description="错误信息")
    remark: str | None = Field(None, description="备注")


class StockMonitorLogOut(BaseModel):
    """股票监听日志输出"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    strategy_id: int
    strategy_name: str
    user_id: int
    stock_code: str
    stock_name: str | None = None
    strategy_type: str
    trigger_time: datetime
    trigger_count: int
    trigger_condition: str | None = None
    trigger_value: float | None = None
    trigger_percent: float | None = None
    price: float | None = None
    change_percent: float | None = None
    volume: int | None = None
    turnover_rate: float | None = None
    notify_status: int
    notify_time: datetime | None = None
    notify_method: str | None = None
    notify_content: str | None = None
    notify_result: str | None = None
    error_message: str | None = None
    strategy_config_snapshot: str | None = None
    remark: str | None = None
    created_at: DatetimeStr
    updated_at: DatetimeStr


class StockMonitorLogStatistics(BaseModel):
    """日志统计信息"""

    total_triggers: int = Field(0, description="总触发次数")
    success_notifications: int = Field(0, description="成功推送次数")
    failed_notifications: int = Field(0, description="失败推送次数")
    monitored_stocks: int = Field(0, description="监控股票数")
    period_days: int = Field(7, description="统计周期（天）")
