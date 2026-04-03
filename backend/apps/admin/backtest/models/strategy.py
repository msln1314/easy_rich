#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version : 1.0
# @Create Time : 2026/4/4
# @File : strategy.py
# @IDE : PyCharm
# @desc : 回测策略模型

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, DateTime, Integer, Text, JSON


class BacktestStrategy(BaseModel):
    """回测策略表"""
    __tablename__ = "backtest_strategy"
    __table_args__ = (
        {"comment": "回测策略表"},
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="策略名称")
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="策略描述")
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="创建者ID")
    strategy_type: Mapped[str] = mapped_column(
        String(20), nullable=False, default="custom",
        comment="策略类型: technical/factor/event/ml/custom"
    )
    strategy_code: Mapped[str | None] = mapped_column(Text, nullable=True, comment="策略Python代码")
    strategy_config: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="参数化配置")
    template_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="关联模板ID")
    data_source: Mapped[str] = mapped_column(
        String(20), nullable=False, default="gm",
        comment="数据源: gm/local/akshare/custom"
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="draft",
        comment="状态: draft/published/archived"
    )
    tags: Mapped[list | None] = mapped_column(JSON, nullable=True, comment="标签列表")