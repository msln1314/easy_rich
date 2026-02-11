#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/31
# @File           : stock_board_industry.py
# @IDE            : PyCharm
# @desc           : 股票行业板块模型 - 同花顺行业一览表

from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, DateTime, Integer, Float, Index, UniqueConstraint


class StockBoardIndustry(BaseModel):
    __tablename__ = "stock_board_industry"
    __table_args__ = (
        UniqueConstraint('board_name', 'date_at', name='uk_board_industry_name_date'),
        Index('idx_board_name', 'board_name'),
        Index('idx_date_at', 'date_at'),
        Index('idx_change_percent', 'change_percent'),
        Index('idx_net_inflow', 'net_inflow'),
        Index('idx_created_at', 'created_at'),
        {'comment': '股票行业板块表（同花顺行业一览表）'}
    )

    # 基础信息
    board_name: Mapped[str] = mapped_column(String(50), nullable=False, comment="板块名称")
    board_code: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="板块代码")
    sequence: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="序号")

    # 价格信息
    change_percent: Mapped[float | None] = mapped_column(Float, nullable=True, comment="涨跌幅（%）")
    average_price: Mapped[float | None] = mapped_column(Float, nullable=True, comment="均价")

    # 成交信息
    total_volume: Mapped[float | None] = mapped_column(Float, nullable=True, comment="总成交量（万手）")
    total_amount: Mapped[float | None] = mapped_column(Float, nullable=True, comment="总成交额（亿元）")

    # 资金流向
    net_inflow: Mapped[float | None] = mapped_column(Float, nullable=True, comment="净流入（亿元）")

    # 涨跌统计
    up_count: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="上涨家数")
    down_count: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="下跌家数")

    # 领涨股信息
    leading_stock: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="领涨股")
    leading_stock_price: Mapped[float | None] = mapped_column(Float, nullable=True, comment="领涨股最新价")
    leading_stock_change: Mapped[float | None] = mapped_column(Float, nullable=True, comment="领涨股涨跌幅（%）")
    leading_stock_code: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="领涨股代码")

    # 时间信息
    date_at: Mapped[date] = mapped_column(DateTime, nullable=False, comment="数据日期")
    data_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="数据时间（采集时间）")

    # 数据来源
    data_from: Mapped[str | None] = mapped_column(String(50), nullable=True, default="akshare_ths", comment="数据来源：akshare_ths")
