#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/31
# @File           : stock_board_concept.py
# @IDE            : PyCharm
# @desc           : 股票概念板块模型 - 东方财富概念板块表

from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, DateTime, Integer, Float, Index, UniqueConstraint


class StockBoardConcept(BaseModel):
    __tablename__ = "stock_board_concept"
    __table_args__ = (
        UniqueConstraint("concept_name", "date_at", name="uk_concept_name_date"),
        Index("idx_concept_name", "concept_name"),
        Index("idx_date_at", "date_at"),
        Index("idx_change_percent", "change_percent"),
        Index("idx_net_inflow", "net_inflow"),
        Index("idx_created_at", "created_at"),
        {"comment": "股票概念板块表（东方财富概念板块）"},
    )

    # 基础信息
    concept_name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="概念名称"
    )
    concept_code: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="概念代码"
    )
    sequence: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="序号")

    # 价格信息
    change_percent: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="涨跌幅（%）"
    )
    average_price: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="均价"
    )

    # 成交信息
    total_volume: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="总成交量（万手）"
    )
    total_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="总成交额（亿元）"
    )

    # 资金流向
    net_inflow: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="净流入（亿元）"
    )
    main_inflow: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="主力净流入（亿元）"
    )
    super_inflow: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="超大单净流入（亿元）"
    )
    big_inflow: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="大单净流入（亿元）"
    )
    mid_inflow: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="中单净流入（亿元）"
    )
    small_inflow: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="小单净流入（亿元）"
    )

    # 涨跌统计
    up_count: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="上涨家数"
    )
    down_count: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="下跌家数"
    )
    flat_count: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="平盘家数"
    )

    # 领涨股信息
    leading_stock: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="领涨股"
    )
    leading_stock_price: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="领涨股最新价"
    )
    leading_stock_change: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="领涨股涨跌幅（%）"
    )
    leading_stock_code: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="领涨股代码"
    )

    # 时间信息
    date_at: Mapped[date] = mapped_column(DateTime, nullable=False, comment="数据日期")
    data_time: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="数据时间（采集时间）"
    )

    # 数据来源
    data_from: Mapped[str | None] = mapped_column(
        String(50), nullable=True, default="akshare_em", comment="数据来源：akshare_em"
    )

    # 市场表现指标
    turnover_rate: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="换手率（%）"
    )
    pe_ratio: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="市盈率"
    )
    pb_ratio: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="市净率"
    )
    market_cap: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="总市值（亿元）"
    )

    # 公司数量
    stock_count: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="成分股数量"
    )

    # 最新价格信息
    latest_price: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="最新指数点位"
    )
    open_price: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="开盘点位"
    )
    high_price: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="最高点位"
    )
    low_price: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="最低点位"
    )
    prev_close: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="昨收点位"
    )
