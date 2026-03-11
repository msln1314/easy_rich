#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version : 1.0
# @Create Time : 2026/3/8
# @File : stock_daily_ranking.py
# @IDE : PyCharm
# @desc : 个股每日排行 Pydantic 模型

from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr
from datetime import date


class StockDailyRankingOut(BaseModel):
    """每日排行数据输出"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    stock_code: str | None = Field(None, description="股票代码")
    stock_name: str | None = Field(None, description="股票名称")
    full_code: str | None = Field(None, description="完整股票代码")

    ranking_type: str = Field(..., description="排行类型")
    rank: int = Field(..., description="当日排名")
    rank_change: int | None = Field(None, description="排名变化")

    ranking_value: float | None = Field(None, description="排行指标值")
    ranking_value_unit: str | None = Field(None, description="数值单位")

    market: str | None = Field(None, description="市场类型")
    industry: str | None = Field(None, description="所属行业")

    current_price: float | None = Field(None, description="最新价")
    change_percent: float | None = Field(None, description="涨跌幅(%)")
    change_amount: float | None = Field(None, description="涨跌额")

    volume: float | None = Field(None, description="成交量(手)")
    amount: float | None = Field(None, description="成交额(元)")
    turnover_rate: float | None = Field(None, description="换手率(%)")

    total_market_cap: float | None = Field(None, description="总市值(元)")
    circulating_market_cap: float | None = Field(None, description="流通市值(元)")

    hot_value: float | None = Field(None, description="热度值")
    hot_rank_change: int | None = Field(None, description="热度排名变化")

    data_date: date
    data_source: str | None = Field(None, description="数据来源")

    created_at: DatetimeStr
    updated_at: DatetimeStr


class StockDailyRankingListOut(BaseModel):
    """每日排行列表输出"""

    items: list[StockDailyRankingOut]
    total: int
    page: int
    page_size: int
    ranking_type: str
    data_date: date | None = None


class StockRankingTrendOut(BaseModel):
    """排行趋势数据输出"""

    stock_code: str = Field(..., description="股票代码")
    stock_name: str | None = Field(None, description="股票名称")
    ranking_type: str = Field(..., description="排行类型")
    trend_data: list = Field(default_factory=list, description="趋势数据列表")


class StockRankingSummaryOut(BaseModel):
    """排行榜单汇总输出"""

    ranking_type: str = Field(..., description="排行类型")
    data_date: date = Field(..., description="数据日期")
    total_count: int = Field(..., description="当日上榜股票总数")
    top_stocks: list = Field(default_factory=list, description="前十名股票")


class HotRankingOut(BaseModel):
    """热度排行数据输出"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    stock_code: str | None = Field(None, description="股票代码")
    stock_name: str | None = Field(None, description="股票名称")
    full_code: str | None = Field(None, description="完整股票代码")

    rank: int = Field(..., description="当前热度排名")
    rank_change: int | None = Field(None, description="排名变化")

    current_price: float | None = Field(None, description="最新价")
    change_percent: float | None = Field(None, description="涨跌幅(%)")

    hot_value: float | None = Field(None, description="热度值")
    hot_value_change: float | None = Field(None, description="热度值变化")

    volume: float | None = Field(None, description="成交量")
    amount: float | None = Field(None, description="成交额")
    turnover_rate: float | None = Field(None, description="换手率")

    fans_count: int | None = Field(None, description="粉丝数量")
    view_count: int | None = Field(None, description="浏览量")
    comment_count: int | None = Field(None, description="评论数")

    data_date: date
    data_time: DatetimeStr | None = Field(None, description="数据时间")

    created_at: DatetimeStr
