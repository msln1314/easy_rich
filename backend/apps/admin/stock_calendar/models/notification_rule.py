# -*- coding: utf-8 -*-
"""通知规则模型 - 用于财经日历"""
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Integer, Text, Date, Index
from db.db_base import BaseModel


class NotificationRule(BaseModel):
    """通知规则表"""
    __tablename__ = "stock_notification_rule"
    __table_args__ = (
        Index("idx_user_enabled", "user_id", "is_enabled"),
        Index("idx_rule_type", "rule_type"),
        {"comment": "股票通知规则表"},
    )

    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="用户ID")
    rule_name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="规则名称"
    )
    rule_type: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="规则类型: holiday/earnings/dividend/unlock/custom"
    )
    # 规则类型说明:
    # holiday: 节假日提醒 (如节假日前N天提醒空仓)
    # earnings: 财报发布提醒
    # dividend: 分红除权提醒
    # unlock: 解禁日提醒
    # custom: 自定义规则

    event_type_filter: Mapped[str | None] = mapped_column(
        String(100), nullable=True, comment="事件类型过滤(逗号分隔)"
    )
    stock_codes: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="股票代码列表JSON(为空则全部)"
    )

    condition_config: Mapped[dict | None] = mapped_column(
        Text, nullable=True, comment="条件配置JSON"
    )
    # 示例:
    # {
    #   "days_before": 2,           # 提前N天提醒
    #   "days_after": null,         # 之后N天提醒
    #   "importance_min": 3,        # 最低重要程度
    #   "watchlist_only": true,     # 仅自选股
    #   "specific_dates": []        # 特定日期列表
    # }

    action_config: Mapped[dict | None] = mapped_column(
        Text, nullable=True, comment="动作配置JSON"
    )
    # 示例:
    # {
    #   "message": "建议节前空仓",   # 提醒消息
    #   "channels": ["email", "wechat"],  # 通知渠道
    #   "template_code": "holiday_empty"  # 使用的模板编码
    # }

    priority: Mapped[int] = mapped_column(
        Integer, default=0, comment="优先级(越大越优先)"
    )
    is_enabled: Mapped[bool] = mapped_column(
        Boolean, default=True, comment="是否启用"
    )
    valid_from: Mapped[date | None] = mapped_column(
        Date, nullable=True, comment="有效期开始"
    )
    valid_to: Mapped[date | None] = mapped_column(
        Date, nullable=True, comment="有效期结束"
    )
    last_triggered_at: Mapped[str | None] = mapped_column(
        String(30), nullable=True, comment="上次触发时间"
    )