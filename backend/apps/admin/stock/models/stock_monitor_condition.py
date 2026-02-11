#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/28
# @File           : stock_monitor_condition.py
# @IDE            : PyCharm
# @desc           : 股票监控配置模型

from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, DateTime, Integer, Index


class StockMonitorCondition(BaseModel):
    __tablename__ = "stock_monitor_condition"
    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_is_active', 'is_active'),
        {'comment': '股票监控配置表'}
    )

    condition_content: Mapped[str] = mapped_column(String(1024), nullable=False, comment="股票代码")
    tag: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="股票名称")
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="监控名称/描述")
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="创建用户ID")
    is_active: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="是否启用：1启用 0禁用")
    remark: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="备注")
    owner: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="拥有者")
    reason: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="条件原因")
    watch_days: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="关注7天")
