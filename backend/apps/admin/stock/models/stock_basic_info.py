#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/7/7 13:41
# @File           : stock_basic_info.py
# @IDE            : PyCharm
# @desc           : 股票基本信息模型

from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, DateTime, Index, Float


class StockBasicInfo(BaseModel):
    __tablename__ = "stock_basic_info"
    __table_args__ = (
        Index('idx_full_code', 'full_code'),
        {'comment': '股票基本信息表'}
    )

    full_code: Mapped[str] = mapped_column(String(20), nullable=False, comment="TS 股票代码")
    stock_code: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="股票代码")
    stock_name: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="股票名称")
    full_name: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="公司名称")
    area: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="地域")
    industry: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="所属行业")
    board: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="板块:主板，科创板，创业板")
    cnspell: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="拼音缩写")
    market: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="市场类型")
    list_date: Mapped[date | None] = mapped_column(DateTime, nullable=True, comment="上市日期")
    total_shares: Mapped[float | None] = mapped_column(Float, nullable=True, comment="A股总股本")
    circulating_shares: Mapped[float | None] = mapped_column(Float, nullable=True, comment="A股流通股本")
    act_name: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="实际控制人名称")
    act_ent_type: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="实际控制人企业类型")
    is_hs: Mapped[str | None] = mapped_column(String(10), nullable=True, comment="是否沪深港通标的，N否 H沪股通 S深股通")
    delist_date: Mapped[date | None] = mapped_column(DateTime, nullable=True, comment="退市日期")
    status: Mapped[str | None] = mapped_column(String(10), nullable=True, comment="上市状态：L上市 D退市 P暂停上市")
    trade_status: Mapped[str | None] = mapped_column(String(10), nullable=True, comment="交易状态：交易中 ，停牌")

    # 实时行情字段
    current_price: Mapped[float | None] = mapped_column(Float, nullable=True, comment="最新价")
    change_percent: Mapped[float | None] = mapped_column(Float, nullable=True, comment="涨跌幅(%)")
    change_amount: Mapped[float | None] = mapped_column(Float, nullable=True, comment="涨跌额")
    volume: Mapped[float | None] = mapped_column(Float, nullable=True, comment="成交量(手)")
    amount: Mapped[float | None] = mapped_column(Float, nullable=True, comment="成交额(元)")
    amplitude: Mapped[float | None] = mapped_column(Float, nullable=True, comment="振幅(%)")
    high_price: Mapped[float | None] = mapped_column(Float, nullable=True, comment="最高价")
    low_price: Mapped[float | None] = mapped_column(Float, nullable=True, comment="最低价")
    open_price: Mapped[float | None] = mapped_column(Float, nullable=True, comment="今开")
    close_price: Mapped[float | None] = mapped_column(Float, nullable=True, comment="昨收")
    volume_ratio: Mapped[float | None] = mapped_column(Float, nullable=True, comment="量比")
    turnover_rate: Mapped[float | None] = mapped_column(Float, nullable=True, comment="换手率(%)")
    pe_ratio: Mapped[float | None] = mapped_column(Float, nullable=True, comment="市盈率-动态")
    pb_ratio: Mapped[float | None] = mapped_column(Float, nullable=True, comment="市净率")
    total_market_cap: Mapped[float | None] = mapped_column(Float, nullable=True, comment="总市值(元)")
    circulating_market_cap: Mapped[float | None] = mapped_column(Float, nullable=True, comment="流通市值(元)")
    change_speed: Mapped[float | None] = mapped_column(Float, nullable=True, comment="涨速")
    change_5min: Mapped[float | None] = mapped_column(Float, nullable=True, comment="5分钟涨跌(%)")
    change_60day: Mapped[float | None] = mapped_column(Float, nullable=True, comment="60日涨跌幅(%)")
    change_ytd: Mapped[float | None] = mapped_column(Float, nullable=True, comment="年初至今涨跌幅(%)")
