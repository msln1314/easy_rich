#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/8
# @File           : stock_factor.py
# @IDE            : PyCharm
# @desc           : 股票多因子模型

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, DateTime, Float, Integer, Index


class StockFactor(BaseModel):
    """股票多因子数据模型"""

    __tablename__ = "stock_factor"
    __table_args__ = (
        Index("idx_stock_code_date", "stock_code", "trade_date"),
        Index("idx_stock_code", "stock_code"),
        Index("idx_trade_date", "trade_date"),
        Index("idx_composite_score", "composite_score"),
        {"comment": "股票多因子数据表"},
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

    pe: Mapped[float | None] = mapped_column(Float, nullable=True, comment="市盈率(PE)")
    pb: Mapped[float | None] = mapped_column(Float, nullable=True, comment="市净率(PB)")
    ps: Mapped[float | None] = mapped_column(Float, nullable=True, comment="市销率(PS)")
    pcf: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="市现率(PCF)"
    )

    pe_percentile: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="PE历史分位(%)"
    )
    pb_percentile: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="PB历史分位(%)"
    )

    roe: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="净资产收益率(ROE)(%)"
    )
    roa: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="总资产收益率(ROA)(%)"
    )
    gross_margin: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="毛利率(%)"
    )
    net_margin: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="净利率(%)"
    )

    revenue_growth: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="营收增长率(%)"
    )
    profit_growth: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="净利润增长率(%)"
    )

    debt_ratio: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="资产负债率(%)"
    )
    current_ratio: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="流动比率"
    )
    quick_ratio: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="速动比率"
    )

    change_5d: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="5日涨跌幅(%)"
    )
    change_20d: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="20日涨跌幅(%)"
    )
    change_60d: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="60日涨跌幅(%)"
    )
    change_120d: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="120日涨跌幅(%)"
    )

    relative_strength: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="相对强弱(%)"
    )

    value_score: Mapped[float] = mapped_column(
        Float, nullable=False, default=0, comment="价值因子得分"
    )
    growth_score: Mapped[float] = mapped_column(
        Float, nullable=False, default=0, comment="成长因子得分"
    )
    quality_score: Mapped[float] = mapped_column(
        Float, nullable=False, default=0, comment="质量因子得分"
    )
    momentum_score: Mapped[float] = mapped_column(
        Float, nullable=False, default=0, comment="动量因子得分"
    )

    composite_score: Mapped[float] = mapped_column(
        Float, nullable=False, default=0, comment="综合得分"
    )
    composite_rank: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="综合排名"
    )
