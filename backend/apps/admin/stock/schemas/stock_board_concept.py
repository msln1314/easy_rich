#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/31
# @File           : stock_board_concept.py
# @IDE            : PyCharm
# @desc           : 股票概念板块 pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr, DecimalField
from datetime import date, datetime


class StockBoardConceptCreate(BaseModel):
    """创建股票概念板块"""

    concept_name: str = Field(..., description="概念名称")
    concept_code: str | None = Field(None, description="概念代码")
    sequence: int | None = Field(None, description="序号")
    change_percent: float | None = Field(None, description="涨跌幅（%）")
    average_price: float | None = Field(None, description="均价")
    total_volume: float | None = Field(None, description="总成交量（万手）")
    total_amount: float | None = Field(None, description="总成交额（亿元）")
    net_inflow: float | None = Field(None, description="净流入（亿元）")
    main_inflow: float | None = Field(None, description="主力净流入（亿元）")
    super_inflow: float | None = Field(None, description="超大单净流入（亿元）")
    big_inflow: float | None = Field(None, description="大单净流入（亿元）")
    mid_inflow: float | None = Field(None, description="中单净流入（亿元）")
    small_inflow: float | None = Field(None, description="小单净流入（亿元）")
    up_count: int | None = Field(None, description="上涨家数")
    down_count: int | None = Field(None, description="下跌家数")
    flat_count: int | None = Field(None, description="平盘家数")
    leading_stock: str | None = Field(None, description="领涨股")
    leading_stock_price: float | None = Field(None, description="领涨股最新价")
    leading_stock_change: float | None = Field(None, description="领涨股涨跌幅（%）")
    leading_stock_code: str | None = Field(None, description="领涨股代码")
    date_at: date = Field(..., description="数据日期")
    data_time: datetime | None = Field(None, description="数据时间（采集时间）")
    data_from: str | None = Field("akshare_em", description="数据来源")
    turnover_rate: float | None = Field(None, description="换手率（%）")
    pe_ratio: float | None = Field(None, description="市盈率")
    pb_ratio: float | None = Field(None, description="市净率")
    market_cap: float | None = Field(None, description="总市值（亿元）")
    stock_count: int | None = Field(None, description="成分股数量")
    latest_price: float | None = Field(None, description="最新指数点位")
    open_price: float | None = Field(None, description="开盘点位")
    high_price: float | None = Field(None, description="最高点位")
    low_price: float | None = Field(None, description="最低点位")
    prev_close: float | None = Field(None, description="昨收点位")


class StockBoardConceptUpdate(BaseModel):
    """更新股票概念板块"""

    concept_name: str | None = Field(None, description="概念名称")
    concept_code: str | None = Field(None, description="概念代码")
    sequence: int | None = Field(None, description="序号")
    change_percent: float | None = Field(None, description="涨跌幅（%）")
    average_price: float | None = Field(None, description="均价")
    total_volume: float | None = Field(None, description="总成交量（万手）")
    total_amount: float | None = Field(None, description="总成交额（亿元）")
    net_inflow: float | None = Field(None, description="净流入（亿元）")
    main_inflow: float | None = Field(None, description="主力净流入（亿元）")
    super_inflow: float | None = Field(None, description="超大单净流入（亿元）")
    big_inflow: float | None = Field(None, description="大单净流入（亿元）")
    mid_inflow: float | None = Field(None, description="中单净流入（亿元）")
    small_inflow: float | None = Field(None, description="小单净流入（亿元）")
    up_count: int | None = Field(None, description="上涨家数")
    down_count: int | None = Field(None, description="下跌家数")
    flat_count: int | None = Field(None, description="平盘家数")
    leading_stock: str | None = Field(None, description="领涨股")
    leading_stock_price: float | None = Field(None, description="领涨股最新价")
    leading_stock_change: float | None = Field(None, description="领涨股涨跌幅（%）")
    leading_stock_code: str | None = Field(None, description="领涨股代码")
    date_at: date | None = Field(None, description="数据日期")
    data_time: datetime | None = Field(None, description="数据时间（采集时间）")
    data_from: str | None = Field(None, description="数据来源")
    turnover_rate: float | None = Field(None, description="换手率（%）")
    pe_ratio: float | None = Field(None, description="市盈率")
    pb_ratio: float | None = Field(None, description="市净率")
    market_cap: float | None = Field(None, description="总市值（亿元）")
    stock_count: int | None = Field(None, description="成分股数量")
    latest_price: float | None = Field(None, description="最新指数点位")
    open_price: float | None = Field(None, description="开盘点位")
    high_price: float | None = Field(None, description="最高点位")
    low_price: float | None = Field(None, description="最低点位")
    prev_close: float | None = Field(None, description="昨收点位")


class StockBoardConceptOut(BaseModel):
    """股票概念板块输出"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    concept_name: str
    concept_code: str | None = None
    sequence: int | None = None
    change_percent: float | None = None
    average_price: float | None = None
    total_volume: float | None = None
    total_amount: float | None = None
    net_inflow: float | None = None
    main_inflow: float | None = None
    super_inflow: float | None = None
    big_inflow: float | None = None
    mid_inflow: float | None = None
    small_inflow: float | None = None
    up_count: int | None = None
    down_count: int | None = None
    flat_count: int | None = None
    leading_stock: str | None = None
    leading_stock_price: float | None = None
    leading_stock_change: float | None = None
    leading_stock_code: str | None = None
    date_at: DatetimeStr
    data_time: DatetimeStr | None = None
    data_from: str | None = None
    turnover_rate: float | None = None
    pe_ratio: float | None = None
    pb_ratio: float | None = None
    market_cap: float | None = None
    stock_count: int | None = None
    latest_price: float | None = None
    open_price: float | None = None
    high_price: float | None = None
    low_price: float | None = None
    prev_close: float | None = None
    created_at: DatetimeStr
    updated_at: DatetimeStr
