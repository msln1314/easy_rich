#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/21
# @File           : stock_longhubang.py
# @IDE            : PyCharm
# @desc           : 龙虎榜数据模型

from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, DateTime, Float, Integer, Index, Text


class StockLonghubang(BaseModel):
    """
    龙虎榜数据表
    存储每日龙虎榜交易数据
    """

    __tablename__ = "stock_longhubang"
    __table_args__ = (
        Index("idx_lhb_trade_date", "trade_date"),
        Index("idx_lhb_stock_code", "stock_code"),
        Index("idx_lhb_stock_date", "stock_code", "trade_date"),
        {"comment": "龙虎榜数据表"},
    )

    # 交易日期
    trade_date: Mapped[date] = mapped_column(
        DateTime, nullable=False, comment="交易日期"
    )

    # 股票基本信息
    stock_code: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="股票代码"
    )
    stock_name: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="股票名称"
    )
    full_code: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="完整代码"
    )
    market: Mapped[str | None] = mapped_column(
        String(10), nullable=True, comment="市场(SH/SZ)"
    )

    # 价格信息
    close_price: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="收盘价"
    )
    change_percent: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="涨跌幅(%)"
    )
    turnover_rate: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="换手率(%)"
    )

    # 成交信息
    total_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="总成交额(元)"
    )
    net_buy_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="龙虎榜净买额(元)"
    )
    net_buy_ratio: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="龙虎榜净买额占比(%)"
    )

    # 上榜原因
    reason: Mapped[str | None] = mapped_column(
        String(200), nullable=True, comment="上榜原因"
    )

    # 买入营业部详情(JSON格式)
    buy_details: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="买入营业部详情(JSON)"
    )

    # 卖出营业部详情(JSON格式)
    sell_details: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="卖出营业部详情(JSON)"
    )

    # 统计信息
    buy_amount_total: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="买入总额(元)"
    )
    sell_amount_total: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="卖出总额(元)"
    )

    # 数据来源
    data_from: Mapped[str | None] = mapped_column(
        String(50), nullable=True, default="stock_service", comment="数据来源"
    )
    data_time: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="数据生成时间"
    )


class StockLonghubangDetail(BaseModel):
    """
    龙虎榜明细表
    存储龙虎榜买卖营业部明细
    """

    __tablename__ = "stock_longhubang_detail"
    __table_args__ = (
        Index("idx_lhb_detail_date", "trade_date"),
        Index("idx_lhb_detail_stock", "stock_code"),
        Index("idx_lhb_detail_type", "trade_type"),
        {"comment": "龙虎榜明细表"},
    )

    # 关联字段
    longhubang_id: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="关联龙虎榜ID"
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

    # 营业部信息
    trade_type: Mapped[str | None] = mapped_column(
        String(10), nullable=True, comment="交易类型(buy/sell)"
    )
    broker_name: Mapped[str | None] = mapped_column(
        String(100), nullable=True, comment="营业部名称"
    )
    broker_type: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="营业部类型(机构/游资/沪股通等)"
    )

    # 交易数据
    buy_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="买入金额(元)"
    )
    sell_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="卖出金额(元)"
    )
    net_amount: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="净买卖金额(元)"
    )

    # 数据来源
    data_from: Mapped[str | None] = mapped_column(
        String(50), nullable=True, default="stock_service", comment="数据来源"
    )
    data_time: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="数据生成时间"
    )
