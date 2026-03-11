#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/10
# @File           : stock_index.py
# @IDE            : PyCharm
# @desc           : 大盘指数模型

from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import (
    String,
    DateTime,
    Float,
    Integer,
    Index,
    UniqueConstraint,
)


class StockIndex(BaseModel):
    """
    大盘指数表
    存储上证指数、深证成指、创业板指、科创50等主要指数数据
    每日更新，新数据覆盖当日数据
    """

    __tablename__ = "stock_index"
    __table_args__ = (
        UniqueConstraint("index_code", "data_date", name="uk_stock_index_code_date"),
        Index("idx_data_date", "data_date"),
        Index("idx_index_code", "index_code"),
        {"comment": "大盘指数表"},
    )

    # 指数信息
    index_code: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="指数代码（如 000001.SH）"
    )
    index_name: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="指数名称（如 上证指数）"
    )

    # 行情数据
    open_price: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="开盘点位"
    )
    high_price: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="最高点位"
    )
    low_price: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="最低点位"
    )
    close_price: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="收盘点位/最新价"
    )
    pre_close: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="昨收点位"
    )

    # 涨跌数据
    change_percent: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="涨跌幅(%)"
    )
    change_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="涨跌额"
    )

    # 成交数据
    volume: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="成交量(手)"
    )
    amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="成交额(元)"
    )

    # 盘口数据
    turnover_rate: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="换手率(%)"
    )
    amplitude: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="振幅(%)"
    )

    # 指标数据
    pe: Mapped[float | None] = mapped_column(Float, nullable=True, comment="市盈率")
    pb: Mapped[float | None] = mapped_column(Float, nullable=True, comment="市净率")
    total_market_cap: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="总市值(元)"
    )
    circulating_market_cap: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="流通市值(元)"
    )

    # 时间信息
    data_date: Mapped[date] = mapped_column(
        DateTime, nullable=False, comment="数据日期"
    )
    data_time: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="数据时间（采集时间）"
    )

    # 数据来源
    data_source: Mapped[str | None] = mapped_column(
        String(50), nullable=True, default="akshare", comment="数据来源"
    )