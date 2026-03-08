#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/8
# @File           : stock_research.py
# @IDE            : PyCharm
# @desc           : 股票券商研报模型

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, DateTime, Float, Index


class StockResearch(BaseModel):
    """券商研报数据模型"""

    __tablename__ = "stock_research"
    __table_args__ = (
        Index("idx_stock_code_date", "stock_code", "publish_date"),
        Index("idx_stock_code", "stock_code"),
        Index("idx_publish_date", "publish_date"),
        Index("idx_rating", "rating"),
        Index("idx_institution", "institution"),
        {"comment": "券商研报数据表"},
    )

    stock_code: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="股票代码"
    )
    stock_name: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="股票名称"
    )

    institution: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="券商名称"
    )
    researcher: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="研究员"
    )

    publish_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, comment="发布日期"
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False, comment="研报标题")

    rating: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="评级: 买入/增持/中性/减持/卖出"
    )
    rating_change: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="评级变动: 上调/维持/下调"
    )

    target_price: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="目标价格"
    )
    current_price: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="现价"
    )
    target_change_pct: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="目标涨幅(%)"
    )

    report_type: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="研报类型"
    )
    report_url: Mapped[str | None] = mapped_column(
        String(500), nullable=True, comment="研报链接"
    )
