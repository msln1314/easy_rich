#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/31
# @File           : stock_board_industry.py
# @IDE            : PyCharm
# @desc           : 股票行业板块 pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr, DecimalField
from datetime import date, datetime


class StockBoardIndustryCreate(BaseModel):
    """创建股票行业板块"""
    board_name: str = Field(..., description="板块名称")
    board_code: str | None = Field(None, description="板块代码")
    sequence: int | None = Field(None, description="序号")
    change_percent: float | None = Field(None, description="涨跌幅（%）")
    average_price: float | None = Field(None, description="均价")
    total_volume: float | None = Field(None, description="总成交量（万手）")
    total_amount: float | None = Field(None, description="总成交额（亿元）")
    net_inflow: float | None = Field(None, description="净流入（亿元）")
    up_count: int | None = Field(None, description="上涨家数")
    down_count: int | None = Field(None, description="下跌家数")
    leading_stock: str | None = Field(None, description="领涨股")
    leading_stock_price: float | None = Field(None, description="领涨股最新价")
    leading_stock_change: float | None = Field(None, description="领涨股涨跌幅（%）")
    leading_stock_code: str | None = Field(None, description="领涨股代码")
    date_at: date = Field(..., description="数据日期")
    data_time: datetime | None = Field(None, description="数据时间（采集时间）")
    data_from: str | None = Field('akshare_ths', description="数据来源")


class StockBoardIndustryUpdate(BaseModel):
    """更新股票行业板块"""
    board_name: str | None = Field(None, description="板块名称")
    board_code: str | None = Field(None, description="板块代码")
    sequence: int | None = Field(None, description="序号")
    change_percent: float | None = Field(None, description="涨跌幅（%）")
    average_price: float | None = Field(None, description="均价")
    total_volume: float | None = Field(None, description="总成交量（万手）")
    total_amount: float | None = Field(None, description="总成交额（亿元）")
    net_inflow: float | None = Field(None, description="净流入（亿元）")
    up_count: int | None = Field(None, description="上涨家数")
    down_count: int | None = Field(None, description="下跌家数")
    leading_stock: str | None = Field(None, description="领涨股")
    leading_stock_price: float | None = Field(None, description="领涨股最新价")
    leading_stock_change: float | None = Field(None, description="领涨股涨跌幅（%）")
    leading_stock_code: str | None = Field(None, description="领涨股代码")
    date_at: date | None = Field(None, description="数据日期")
    data_time: datetime | None = Field(None, description="数据时间（采集时间）")
    data_from: str | None = Field(None, description="数据来源")


class StockBoardIndustryOut(BaseModel):
    """股票行业板块输出"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    board_name: str
    board_code: str | None = None
    sequence: int | None = None
    change_percent: float | None = None
    average_price: float | None = None
    total_volume: float | None = None
    total_amount: float | None = None
    net_inflow: float | None = None
    up_count: int | None = None
    down_count: int | None = None
    leading_stock: str | None = None
    leading_stock_price: float | None = None
    leading_stock_change: float | None = None
    leading_stock_code: str | None = None
    date_at: DatetimeStr
    data_time: DatetimeStr | None = None
    data_from: str | None = None
    created_at: DatetimeStr
    updated_at: DatetimeStr
