#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/22
# @File           : stock_daily.py
# @IDE            : PyCharm
# @desc           : 股票日线K线数据模型

from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, DateTime, Index, Float, UniqueConstraint


class StockDaily(BaseModel):
    """股票日线K线数据表"""

    __tablename__ = "stock_daily"
    __table_args__ = (
        UniqueConstraint("stock_code", "trade_date", name="idx_stock_date"),
        Index("idx_trade_date", "trade_date"),
        {"comment": "股票日线数据表"},
    )

    stock_code: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="股票代码"
    )
    stock_name: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="股票名称"
    )
    full_code: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="完整代码（如sz.000001）"
    )
    trade_date: Mapped[date] = mapped_column(
        DateTime, nullable=False, comment="交易日期"
    )
    open_price: Mapped[float] = mapped_column(Float, nullable=False, comment="开盘价")
    high_price: Mapped[float] = mapped_column(Float, nullable=False, comment="最高价")
    low_price: Mapped[float] = mapped_column(Float, nullable=False, comment="最低价")
    close_price: Mapped[float] = mapped_column(Float, nullable=False, comment="收盘价")
    volume: Mapped[float] = mapped_column(Float, nullable=False, comment="成交量")
    amount: Mapped[float] = mapped_column(Float, nullable=False, comment="成交额")
    buy_volume: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="外盘"
    )
    sell_volume: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="内盘"
    )
    turnover_rate: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="换手率（百分比）"
    )
    volume_ratio: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="量比"
    )
    total_market_cap: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="总市值（万元）"
    )
    circulating_shares: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="流通股本总额（万股）"
    )
    net_assets: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="净资产（元/股）"
    )
    pe_ratio: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="市盈率"
    )
    amplitude: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="振幅（百分比）"
    )
    change_percent: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="涨跌幅（百分比）"
    )
    change_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="涨跌额（元）"
    )
    average_price: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="均价"
    )
    previous_close: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="昨收价"
    )
    limit_up: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="涨停价"
    )
    limit_down: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="跌停价"
    )
    data_source: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="数据来源"
    )
