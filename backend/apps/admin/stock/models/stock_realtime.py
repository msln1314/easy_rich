#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/2/8
# @File           : stock_realtime.py
# @IDE            : PyCharm
# @desc           : 股票实时数据模型

from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, DateTime, Index, Float, Integer


class StockRealtime(BaseModel):
    __tablename__ = "stock_realtime"
    __table_args__ = (
        Index('uk_stock_realtime_time', 'stock_code', 'trade_date', unique=True),
        Index('idx_stock_code', 'stock_code'),
        Index('idx_trade_date', 'trade_date'),
        Index('idx_trade_time', 'trade_time'),
        Index('idx_current_price', 'current_price'),
        Index('idx_change_percent', 'change_percent'),
        Index('idx_volume', 'volume'),
        Index('idx_is_trading', 'is_trading'),
        Index('idx_data_source', 'data_source'),
        {'comment': '股票实时数据表'}
    )

    full_code: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="全部代码")
    stock_code: Mapped[str] = mapped_column(String(20), nullable=False, comment="股票代码")
    trade_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="交易时间")
    trade_date: Mapped[date] = mapped_column(DateTime, nullable=False, comment="交易日期")
    current_price: Mapped[float] = mapped_column(Float, nullable=False, comment="当前价/最新价")
    open_price: Mapped[float] = mapped_column(Float, nullable=False, comment="开盘价")
    high_price: Mapped[float] = mapped_column(Float, nullable=False, comment="最高价")
    low_price: Mapped[float] = mapped_column(Float, nullable=False, comment="最低价")
    previous_close: Mapped[float] = mapped_column(Float, nullable=False, comment="昨收价")
    change_amount: Mapped[float] = mapped_column(Float, nullable=False, comment="涨跌额（元）")
    change_percent: Mapped[float] = mapped_column(Float, nullable=False, comment="涨跌幅（%）")
    volume: Mapped[float] = mapped_column(Float, nullable=False, comment="成交量（手）")
    amount: Mapped[float] = mapped_column(Float, nullable=False, comment="成交额（万元）")
    buy_volume: Mapped[float | None] = mapped_column(Float, nullable=True, comment="外盘/主动性买盘（手）")
    sell_volume: Mapped[float | None] = mapped_column(Float, nullable=True, comment="内盘/主动性卖盘（手）")
    turnover_rate: Mapped[float | None] = mapped_column(Float, nullable=True, comment="换手率（%）")
    volume_ratio: Mapped[float | None] = mapped_column(Float, nullable=True, comment="量比")
    amplitude: Mapped[float | None] = mapped_column(Float, nullable=True, comment="振幅（%）")
    total_market_cap: Mapped[float | None] = mapped_column(Float, nullable=True, comment="总市值（万元）")
    circulating_market_cap: Mapped[float | None] = mapped_column(Float, nullable=True, comment="流通市值（万元）")
    ma5: Mapped[float | None] = mapped_column(Float, nullable=True, comment="5日均线")
    ma10: Mapped[float | None] = mapped_column(Float, nullable=True, comment="10日均线")
    ma20: Mapped[float | None] = mapped_column(Float, nullable=True, comment="20日均线")
    ma30: Mapped[float | None] = mapped_column(Float, nullable=True, comment="30日均线")
    rsi: Mapped[float | None] = mapped_column(Float, nullable=True, comment="RSI相对强弱指标")
    macd_diff: Mapped[float | None] = mapped_column(Float, nullable=True, comment="MACD DIFF值")
    macd_dea: Mapped[float | None] = mapped_column(Float, nullable=True, comment="MACD DEA值")
    macd_bar: Mapped[float | None] = mapped_column(Float, nullable=True, comment="MACD柱状图")
    pe_ratio: Mapped[float | None] = mapped_column(Float, nullable=True, comment="市盈率（动态）")
    pe_ttm: Mapped[float | None] = mapped_column(Float, nullable=True, comment="市盈率（TTM）")
    pb_ratio: Mapped[float | None] = mapped_column(Float, nullable=True, comment="市净率")
    ps_ratio: Mapped[float | None] = mapped_column(Float, nullable=True, comment="市销率")
    bid1_price: Mapped[float | None] = mapped_column(Float, nullable=True, comment="买一价")
    bid1_volume: Mapped[float | None] = mapped_column(Float, nullable=True, comment="买一量（手）")
    ask1_price: Mapped[float | None] = mapped_column(Float, nullable=True, comment="卖一价")
    ask1_volume: Mapped[float | None] = mapped_column(Float, nullable=True, comment="卖一量（手）")
    bid_price_5: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="买五档价格（用逗号分隔）")
    bid_volume_5: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="买五档量（用逗号分隔）")
    ask_price_5: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="卖五档价格（用逗号分隔）")
    ask_volume_5: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="卖五档量（用逗号分隔）")
    limit_up: Mapped[float | None] = mapped_column(Float, nullable=True, comment="涨停价")
    limit_down: Mapped[float | None] = mapped_column(Float, nullable=True, comment="跌停价")
    is_limit_up: Mapped[int | None] = mapped_column(Integer, nullable=True, default=0, comment="是否涨停：0否 1是")
    is_limit_down: Mapped[int | None] = mapped_column(Integer, nullable=True, default=0, comment="是否跌停：0否 1是")
    is_trading: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="是否交易中：0停牌 1交易中")
    trading_status: Mapped[str | None] = mapped_column(String(20), nullable=True, default='normal', comment="交易状态：normal正常/suspend停牌")
    data_source: Mapped[str | None] = mapped_column(String(50), nullable=True, default='tushare', comment="数据来源")
    stock_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="股票名称")
    key: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="键")
