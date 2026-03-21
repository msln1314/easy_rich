#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/21
# @File           : stock_margin.py
# @IDE            : PyCharm
# @desc           : 融资融券数据模型

from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, DateTime, Float, Integer, Index, UniqueConstraint


class StockMarginSummary(BaseModel):
    """
    融资融券汇总历史表
    存储每日融资融券市场汇总数据
    """

    __tablename__ = "stock_margin_summary"
    __table_args__ = (
        UniqueConstraint("trade_date", name="uk_margin_summary_trade_date"),
        Index("idx_margin_summary_date", "trade_date"),
        Index("idx_margin_summary_created", "created_at"),
        {"comment": "融资融券汇总历史表"},
    )

    trade_date: Mapped[date] = mapped_column(
        DateTime, nullable=False, comment="交易日期"
    )

    rzye: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="融资余额(元)"
    )
    rzmre: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="融资买入额(元)"
    )
    rzche: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="融资偿还额(元)"
    )

    rqye: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="融券余额(元)"
    )
    rqmcl: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="融券卖出量(股)"
    )
    rqchl: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="融券偿还量(股)"
    )

    total: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="融资融券余额合计(元)"
    )

    data_time: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="数据时间（采集时间）"
    )
    data_from: Mapped[str | None] = mapped_column(
        String(50), nullable=True, default="stock_service", comment="数据来源"
    )


class StockMarginDetail(BaseModel):
    """
    融资融券明细历史表
    存储每只股票每日的融资融券数据
    """

    __tablename__ = "stock_margin_detail"
    __table_args__ = (
        UniqueConstraint("trade_date", "stock_code", name="uk_margin_detail_date_code"),
        Index("idx_margin_detail_date", "trade_date"),
        Index("idx_margin_detail_code", "stock_code"),
        Index("idx_margin_detail_rzye", "rzye"),
        {"comment": "融资融券明细历史表"},
    )

    trade_date: Mapped[date] = mapped_column(
        DateTime, nullable=False, comment="交易日期"
    )

    stock_code: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="股票代码"
    )
    stock_name: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="股票名称"
    )
    full_code: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="完整代码"
    )

    rzye: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="融资余额(元)"
    )
    rzmre: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="融资买入额(元)"
    )
    rzche: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="融资偿还额(元)"
    )

    rqye: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="融券余额(元)"
    )
    rqmcl: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="融券卖出量(股)"
    )
    rqchl: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="融券偿还量(股)"
    )

    data_time: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="数据时间（采集时间）"
    )
    data_from: Mapped[str | None] = mapped_column(
        String(50), nullable=True, default="stock_service", comment="数据来源"
    )
