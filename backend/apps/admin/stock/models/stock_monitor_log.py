#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version : 1.0
# @Create Time : 2025/02/15
# @File : stock_monitor_log.py
# @IDE : PyCharm
# @desc : 股票监听推送日志模型

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, DateTime, Integer, Float, Index, Text


class StockMonitorLog(BaseModel):
    __tablename__ = "stock_monitor_log"
    __table_args__ = (
        Index("idx_strategy_id", "strategy_id"),
        Index("idx_user_id", "user_id"),
        Index("idx_stock_code", "stock_code"),
        Index("idx_trigger_time", "trigger_time"),
        Index("idx_notify_status", "notify_status"),
        {"comment": "股票监听推送日志表"},
    )

    # 关联信息
    strategy_id: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="监听策略ID"
    )
    strategy_name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="监听策略名称"
    )
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="用户ID")

    # 股票信息
    stock_code: Mapped[str] = mapped_column(
        String(10), nullable=False, comment="股票代码"
    )
    stock_name: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="股票名称"
    )

    # 策略类型
    strategy_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="监听策略类型：limit_up涨停/limit_down跌停/open_board开板/turnover换手/breakout突破/rebound反弹",
    )

    # 触发信息
    trigger_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, comment="触发时间"
    )
    trigger_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="触发时累计次数"
    )

    # 触发条件
    trigger_condition: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="触发条件描述"
    )
    trigger_value: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="触发时的数值"
    )
    trigger_percent: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="触发时的百分比"
    )

    # 股票价格信息
    price: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="触发时股票价格"
    )
    change_percent: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="触发时涨跌幅（%）"
    )
    volume: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="触发时成交量"
    )
    turnover_rate: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="触发时换手率（%）"
    )

    # 推送信息
    notify_status: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="推送状态：0待推送 1推送成功 2推送失败",
    )
    notify_time: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="推送时间"
    )
    notify_method: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="推送方式：system系统消息/email邮件/sms短信/wechat微信",
    )
    notify_content: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="推送内容"
    )
    notify_result: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="推送结果"
    )

    # 错误信息
    error_message: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="错误信息"
    )

    # 策略配置快照
    strategy_config_snapshot: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="触发时的策略配置快照（JSON）"
    )

    # 其他信息
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")
