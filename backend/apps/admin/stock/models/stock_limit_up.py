#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/8
# @File           : stock_limit_up.py
# @IDE            : PyCharm
# @desc           : 股票涨停板模型

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, DateTime, Float, Integer, Index


class StockLimitUp(BaseModel):
    """涨停板数据模型"""

    __tablename__ = "stock_limit_up"
    __table_args__ = (
        Index("idx_stock_code_date", "stock_code", "trade_date"),
        Index("idx_stock_code", "stock_code"),
        Index("idx_trade_date", "trade_date"),
        Index("idx_limit_type", "limit_type"),
        {"comment": "涨停板数据表"},
    )

    stock_code: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="股票代码"
    )
    stock_name: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="股票名称"
    )
    trade_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, comment="交易日期"
    )

    limit_type: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="涨停类型: zt-涨停, dt-跌停, qx-强势"
    )
    limit_price: Mapped[float] = mapped_column(
        Float, nullable=False, comment="涨停价格"
    )
    pre_close: Mapped[float] = mapped_column(Float, nullable=False, comment="前收盘价")

    first_limit_time: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="首次涨停时间"
    )
    last_limit_time: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="最后涨停时间"
    )
    limit_duration: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="涨停持续时间(分钟)"
    )

    seal_amount: Mapped[float] = mapped_column(
        Float, nullable=False, comment="封单金额(元)"
    )
    seal_volume: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="封单量"
    )

    break_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="炸板次数"
    )
    is_broken: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="是否炸板: 0-未炸, 1-已炸"
    )

    turnover_rate: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="换手率(%)"
    )
    volume_ratio: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="量比"
    )

    consecutive_limit: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1, comment="连续涨停天数"
    )
    limit_reason: Mapped[str | None] = mapped_column(
        String(500), nullable=True, comment="涨停原因"
    )

    market_cap: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="总市值(元)"
    )
    float_cap: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="流通市值(元)"
    )
