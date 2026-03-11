#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/10
# @File           : stock_index.py
# @IDE            : PyCharm
# @desc           : 大盘指数 Pydantic 模型

from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr
from datetime import date, datetime
from typing import Optional


class StockIndexOut(BaseModel):
    """大盘指数输出模型"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    index_code: str = Field(..., description="指数代码")
    index_name: Optional[str] = Field(None, description="指数名称")

    open_price: Optional[float] = Field(None, description="开盘点位")
    high_price: Optional[float] = Field(None, description="最高点位")
    low_price: Optional[float] = Field(None, description="最低点位")
    close_price: Optional[float] = Field(None, description="收盘点位/最新价")
    pre_close: Optional[float] = Field(None, description="昨收点位")

    change_percent: Optional[float] = Field(None, description="涨跌幅(%)")
    change_amount: Optional[float] = Field(None, description="涨跌额")

    volume: Optional[float] = Field(None, description="成交量(手)")
    amount: Optional[float] = Field(None, description="成交额(元)")

    turnover_rate: Optional[float] = Field(None, description="换手率(%)")
    amplitude: Optional[float] = Field(None, description="振幅(%)")

    pe: Optional[float] = Field(None, description="市盈率")
    pb: Optional[float] = Field(None, description="市净率")
    total_market_cap: Optional[float] = Field(None, description="总市值(元)")
    circulating_market_cap: Optional[float] = Field(None, description="流通市值(元)")

    data_date: date
    data_time: Optional[datetime] = Field(None, description="数据时间")

    created_at: DatetimeStr
    updated_at: DatetimeStr


class StockIndexListOut(BaseModel):
    """指数列表输出"""

    items: list[StockIndexOut]
    total: int


class StockIndexQuoteOut(BaseModel):
    """指数实时行情输出（精简版，用于大屏展示）"""

    index_code: str = Field(..., description="指数代码")
    index_name: str = Field(..., description="指数名称")
    close_price: Optional[float] = Field(None, description="最新点位")
    change_percent: Optional[float] = Field(None, description="涨跌幅(%)")
    change_amount: Optional[float] = Field(None, description="涨跌额")
    volume: Optional[float] = Field(None, description="成交量")
    amount: Optional[float] = Field(None, description="成交额")


class IndexQuoteResponse(BaseModel):
    """指数行情响应"""

    items: list[StockIndexQuoteOut]
    update_time: datetime = Field(..., description="更新时间")


class MarketSummaryOut(BaseModel):
    """市场汇总数据输出"""

    # 指数数据
    indices: list[StockIndexQuoteOut] = Field(default_factory=list, description="主要指数")

    # 涨跌统计
    total_stocks: int = Field(0, description="股票总数")
    up_stocks: int = Field(0, description="上涨家数")
    down_stocks: int = Field(0, description="下跌家数")
    flat_stocks: int = Field(0, description="平盘家数")

    # 成交数据
    total_amount: float = Field(0, description="总成交额(元)")
    total_volume: float = Field(0, description="总成交量(手)")

    # 涨跌停
    limit_up_count: int = Field(0, description="涨停家数")
    limit_down_count: int = Field(0, description="跌停家数")

    # 市场时间
    trade_date: date = Field(..., description="交易日期")
    update_time: datetime = Field(..., description="更新时间")


class StockRankingItemOut(BaseModel):
    """排行数据项"""

    rank: int = Field(..., description="排名")
    stock_code: str = Field(..., description="股票代码")
    stock_name: str = Field(..., description="股票名称")
    current_price: Optional[float] = Field(None, description="最新价")
    change_percent: Optional[float] = Field(None, description="涨跌幅(%)")
    volume: Optional[float] = Field(None, description="成交量")
    amount: Optional[float] = Field(None, description="成交额")
    turnover_rate: Optional[float] = Field(None, description="换手率(%)")
    industry: Optional[str] = Field(None, description="所属行业")
    market: Optional[str] = Field(None, description="市场")


class RealtimeRankingsOut(BaseModel):
    """实时排行输出"""

    change_percent_ranking: list[StockRankingItemOut] = Field(
        default_factory=list, description="涨跌幅排行"
    )
    turnover_ranking: list[StockRankingItemOut] = Field(
        default_factory=list, description="换手率排行"
    )
    volume_ranking: list[StockRankingItemOut] = Field(
        default_factory=list, description="成交量排行"
    )
    amount_ranking: list[StockRankingItemOut] = Field(
        default_factory=list, description="成交额排行"
    )
    update_time: datetime = Field(..., description="更新时间")