#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/8
# @File           : stock_margin.py
# @IDE            : PyCharm
# @desc           : 股票融资融券模型

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, DateTime, Float, Integer, Index


class StockMargin(BaseModel):
    """融资融券数据模型"""

    __tablename__ = "stock_margin"
    __table_args__ = (
        Index("idx_stock_code_date", "stock_code", "trade_date"),
        Index("idx_stock_code", "stock_code"),
        Index("idx_trade_date", "trade_date"),
        {"comment": "融资融券数据表"},
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

    margin_balance: Mapped[float] = mapped_column(
        Float, nullable=False, comment="融资余额(元)"
    )
    margin_buy: Mapped[float] = mapped_column(
        Float, nullable=False, comment="融资买入额(元)"
    )
    margin_repay: Mapped[float] = mapped_column(
        Float, nullable=False, comment="融资偿还额(元)"
    )

    short_balance: Mapped[float] = mapped_column(
        Float, nullable=False, comment="融券余额(元)"
    )
    short_sell: Mapped[float] = mapped_column(
        Float, nullable=False, comment="融券卖出量"
    )
    short_repay: Mapped[float] = mapped_column(
        Float, nullable=False, comment="融券偿还量"
    )

    margin_net: Mapped[float] = mapped_column(
        Float, nullable=False, comment="融资净买入(元)"
    )
    short_net: Mapped[float] = mapped_column(
        Float, nullable=False, comment="融券净卖出(量)"
    )

    margin_ratio: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="融资占比(%)"
    )
    short_ratio: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="融券占比(%)"
    )

    total_balance: Mapped[float] = mapped_column(
        Float, nullable=False, comment="两融余额(元)"
    )
    total_change: Mapped[float] = mapped_column(
        Float, nullable=False, comment="两融变化(元)"
    )


class StockMarginMarket(BaseModel):
    """市场融资融券汇总模型"""

    __tablename__ = "stock_margin_market"
    __table_args__ = (
        Index("idx_trade_date", "trade_date"),
        {"comment": "市场融资融券汇总表"},
    )

    trade_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, comment="交易日期"
    )

    margin_balance: Mapped[float] = mapped_column(
        Float, nullable=False, comment="融资余额(亿元)"
    )
    margin_buy: Mapped[float] = mapped_column(
        Float, nullable=False, comment="融资买入额(亿元)"
    )
    margin_repay: Mapped[float] = mapped_column(
        Float, nullable=False, comment="融资偿还额(亿元)"
    )

    short_balance: Mapped[float] = mapped_column(
        Float, nullable=False, comment="融券余额(亿元)"
    )
    short_sell: Mapped[float] = mapped_column(
        Float, nullable=False, comment="融券卖出额(亿元)"
    )
    short_repay: Mapped[float] = mapped_column(
        Float, nullable=False, comment="融券偿还额(亿元)"
    )

    total_balance: Mapped[float] = mapped_column(
        Float, nullable=False, comment="两融余额(亿元)"
    )
    total_change: Mapped[float] = mapped_column(
        Float, nullable=False, comment="两融变化(亿元)"
    )

    margin_change_pct: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="融资变化(%)"
    )
    total_change_pct: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="两融变化(%)"
    )
