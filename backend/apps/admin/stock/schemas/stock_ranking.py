#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/1
# @File           : stock_ranking.py
# @IDE            : PyCharm
# @desc           : 个股排行 Pydantic 模型

from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr, FloatStr


class StockRankingOut(BaseModel):
    """个股排行数据输出"""
    model_config = ConfigDict(from_attributes=True)

    rank: int = Field(..., description="排名")
    id: int
    stock_code: str | None = Field(None, description="股票代码")
    stock_name: str | None = Field(None, description="股票名称")
    industry: str | None = Field(None, description="所属行业")
    board: str | None = Field(None, description="板块")
    market: str | None = Field(None, description="市场类型")

    # 价格相关
    current_price: float | None = Field(None, description="最新价")
    change_percent: float | None = Field(None, description="涨跌幅(%)")
    change_amount: float | None = Field(None, description="涨跌额")
    open_price: float | None = Field(None, description="今开")
    high_price: float | None = Field(None, description="最高价")
    low_price: float | None = Field(None, description="最低价")
    close_price: float | None = Field(None, description="昨收")

    # 交易数据
    volume: float | None = Field(None, description="成交量(手)")
    amount: float | None = Field(None, description="成交额(元)")
    turnover_rate: float | None = Field(None, description="换手率(%)")
    volume_ratio: float | None = Field(None, description="量比")

    # 估值数据
    total_market_cap: float | None = Field(None, description="总市值(元)")
    circulating_market_cap: float | None = Field(None, description="流通市值(元)")
    pe_ratio: float | None = Field(None, description="市盈率")
    pb_ratio: float | None = Field(None, description="市净率")

    # 其他指标
    amplitude: float | None = Field(None, description="振幅(%)")
    change_speed: float | None = Field(None, description="涨速")
    change_5min: float | None = Field(None, description="5分钟涨跌(%)")
    change_60day: float | None = Field(None, description="60日涨跌幅(%)")
    change_ytd: float | None = Field(None, description="年初至今涨跌幅(%)")

    created_at: DatetimeStr
    updated_at: DatetimeStr


class StockRankingListOut(BaseModel):
    """排行列表输出"""
    items: list[StockRankingOut]
    total: int
    page: int
    page_size: int
    ranking_type: str
    order: str
