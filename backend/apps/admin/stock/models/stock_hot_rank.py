#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/31
# @File           : stock_hot_rank.py
# @IDE            : PyCharm
# @desc           : 股票人气榜模型 - 东方财富网个股人气榜实时排名

from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, DateTime, Integer, Float, Index, UniqueConstraint


class StockHotRank(BaseModel):
    __tablename__ = "stock_hot_rank"
    __table_args__ = (
        UniqueConstraint('stock_code', 'data_date', name='uk_stock_hot_rank_code_date'),
        Index('idx_stock_code', 'stock_code'),
        Index('idx_stock_name', 'stock_name'),
        Index('idx_data_date', 'data_date'),
        Index('idx_rank', 'rank'),
        Index('idx_change_percent', 'change_percent'),
        Index('idx_created_at', 'created_at'),
        {'comment': '股票人气榜实时排名表'}
    )

    # 基础信息
    stock_code: Mapped[str] = mapped_column(String(20), nullable=False, comment="股票代码，带市场标识（如SZ000001、SH600000）")
    stock_name: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="股票名称")
    full_code: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="TS 股票代码")

    # 排名信息
    rank: Mapped[int] = mapped_column(Integer, nullable=False, comment="当前人气排名（1-100）")
    rank_change: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="排名变化（与上一交易日对比）")

    # 价格信息
    current_price: Mapped[float | None] = mapped_column(Float, nullable=True, comment="最新价（元）")
    change_amount: Mapped[float | None] = mapped_column(Float, nullable=True, comment="涨跌额（元）")
    change_percent: Mapped[float | None] = mapped_column(Float, nullable=True, comment="涨跌幅（%）")

    # 市场信息
    market: Mapped[str | None] = mapped_column(String(10), nullable=True, comment="市场类型：SZ深交所/SH上交所")

    # 时间信息
    data_date: Mapped[date] = mapped_column(DateTime, nullable=False, comment="数据日期")
    data_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="数据时间（采集时间）")

    # 数据来源
    data_from: Mapped[str | None] = mapped_column(String(50), nullable=True, default="akshare", comment="数据来源：akshare")
