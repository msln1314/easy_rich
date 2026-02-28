#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/02/15
# @File           : stock_monitor_strategy.py
# @IDE            : PyCharm
# @desc           : 股票监听策略模型

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, DateTime, Integer, Float, Index, Text


class StockMonitorStrategy(BaseModel):
    __tablename__ = "stock_monitor_strategy"
    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_is_active', 'is_active'),
        Index('idx_strategy_type', 'strategy_type'),
        Index('idx_last_trigger_time', 'last_trigger_time'),
        {'comment': '股票监听策略表'}
    )

    # 基础信息
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="监听策略名称")
    tag: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="标签")
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="创建用户ID")
    
    # 监听股票配置
    stock_code: Mapped[str] = mapped_column(String(10), nullable=True, comment="监听股票代码，如000001")
    stock_name: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="监听股票名称")

    # 策略配置
    strategy_type: Mapped[str] = mapped_column(String(50), nullable=False, comment="监听策略类型：limit_up涨停/limit_down跌停/open_board开板/turnover换手/breakout突破/rebound反弹")

    # 触发条件配置
    condition_content: Mapped[str] = mapped_column(Text, nullable=True, comment="监听条件内容，如换手率>5等")

    # 数值型触发条件
    trigger_value_min: Mapped[float | None] = mapped_column(Float, nullable=True, comment="触发值最小值，如换手率5表示>5%")
    trigger_value_max: Mapped[float | None] = mapped_column(Float, nullable=True, comment="触发值最大值，如换手率10表示<10%")
    trigger_percent_min: Mapped[float | None] = mapped_column(Float, nullable=True, comment="触发百分比最小值，如涨幅5表示>5%")
    trigger_percent_max: Mapped[float | None] = mapped_column(Float, nullable=True, comment="触发百分比最大值，如涨幅10表示<10%")

    # 冷却时间配置（防止频繁触发）
    cooldown_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=60, comment="冷却时间（分钟），触发后多久再次触发")
    cooldown_type: Mapped[str] = mapped_column(String(50), nullable=False, default="same_day", comment="冷却类型：same_day同一天内只触发一次/interval按间隔时间触发")

    # 触发记录
    last_trigger_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="最后触发时间")
    last_trigger_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="上次触发次数")
    trigger_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="累计触发次数")

    # 状态配置
    is_active: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="是否启用：1启用 0禁用")
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=3, comment="优先级：1高 2中 3低")

    # 其他信息
    reason: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="监听原因")
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")

    # 推送配置
    notify_enabled: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="是否启用推送：1启用 0禁用")
    notify_method: Mapped[str] = mapped_column(String(50), nullable=False, default="system", comment="推送方式：system系统消息/email邮件/sms短信/wechat微信")
    notify_trigger_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="推送触发条件：累计触发次数达到此值时才推送，默认1表示每次都推送")
    notify_type: Mapped[str] = mapped_column(String(50), nullable=False, default="once", comment="推送类型：once仅一次/always每次都推送/interval按间隔推送")

    # 策略特定配置（JSON格式）
    strategy_config: Mapped[str | None] = mapped_column(Text, nullable=True, comment="策略特定配置，JSON格式存储，如：{\"threshold\": 9.9, \"direction\": \"up\"}")
