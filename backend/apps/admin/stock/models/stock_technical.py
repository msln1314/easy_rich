#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/1
# @File           : stock_technical.py
# @IDE            : PyCharm
# @desc           : 股票技术分析模型

from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, DateTime, Float, Index, UniqueConstraint


class StockChipDistribution(BaseModel):
    """筹码分布模型"""
    __tablename__ = "stock_chip_distribution"
    __table_args__ = (
        UniqueConstraint('stock_code', 'trade_date', name='uk_stock_chip_distribution'),
        Index('idx_stock_code', 'stock_code'),
        Index('idx_trade_date', 'trade_date'),
        Index('idx_profit_ratio', 'profit_ratio'),
        Index('idx_avg_cost', 'avg_cost'),
        {'comment': '股票筹码分布表'}
    )

    # 基础信息
    stock_code: Mapped[str] = mapped_column(String(20), nullable=False, comment="股票代码")
    full_code: Mapped[str] = mapped_column(String(20), nullable=False, comment="股票代码")
    stock_name: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="股票名称")
    
    # 交易日期
    trade_date: Mapped[date] = mapped_column(DateTime, nullable=False, comment="交易日期")
    
    # 筹码分布数据
    profit_ratio: Mapped[float] = mapped_column(Float, nullable=False, comment="获利比例(%)")
    avg_cost: Mapped[float] = mapped_column(Float, nullable=False, comment="平均成本")
    
    # 90%成本区间
    cost_90_low: Mapped[float] = mapped_column(Float, nullable=False, comment="90成本-低")
    cost_90_high: Mapped[float] = mapped_column(Float, nullable=False, comment="90成本-高")
    concentration_90: Mapped[float] = mapped_column(Float, nullable=False, comment="90集中度(%)")
    
    # 70%成本区间
    cost_70_low: Mapped[float] = mapped_column(Float, nullable=False, comment="70成本-低")
    cost_70_high: Mapped[float] = mapped_column(Float, nullable=False, comment="70成本-高")
    concentration_70: Mapped[float] = mapped_column(Float, nullable=False, comment="70集中度(%)")
    
    # 时间信息
    data_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="数据时间（采集时间）")
    
    # 数据来源
    data_from: Mapped[str | None] = mapped_column(String(50), nullable=True, default="akshare", comment="数据来源：akshare")
