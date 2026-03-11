#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version : 1.0
# @Create Time : 2026/3/8
# @File : stock_daily_ranking.py
# @IDE : PyCharm
# @desc : 个股每日排行查询参数

from enum import Enum
from fastapi import Query, Depends
from core.dependencies import Paging, QueryParams
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class DailyRankingType(str, Enum):
    """每日排行类型"""

    VOLUME = "volume"  # 成交量
    TURNOVER = "turnover"  # 换手率
    AMOUNT = "amount"  # 成交额
    CHANGE_PERCENT = "change_percent"  # 涨跌幅
    HOT = "hot"  # 热度


class RankingOrder(str, Enum):
    """排序方向"""

    DESC = "desc"
    ASC = "asc"


class StockDailyRankingParams(QueryParams):
    """每日排行查询参数"""

    def __init__(
        self,
        ranking_type: DailyRankingType = Query(
            DailyRankingType.TURNOVER, title="排行类型"
        ),
        data_date: Optional[date] = Query(
            None, title="数据日期", description="默认查询最新日期"
        ),
        industry: Optional[str] = Query(None, title="所属行业"),
        market: Optional[str] = Query(None, title="市场类型"),
        stock_code: Optional[str] = Query(None, title="股票代码"),
        stock_name: Optional[str] = Query(None, title="股票名称"),
        params: Paging = Depends(),
    ):
        super().__init__(params)
        self.ranking_type = ranking_type
        self.data_date = data_date
        self.industry = industry
        self.market = market
        self.stock_code = stock_code
        self.stock_name = ("like", stock_name) if stock_name else None


class RankingTrendParams(BaseModel):
    """排行趋势查询参数"""

    stock_code: str = Field(..., description="股票代码")
    ranking_type: DailyRankingType = Field(
        DailyRankingType.TURNOVER, description="排行类型"
    )
    start_date: Optional[date] = Field(None, description="开始日期")
    end_date: date = Field(default_factory=date.today, description="结束日期")


class HotRankingParams(QueryParams):
    """热度排行查询参数"""

    def __init__(
        self,
        data_date: Optional[date] = Query(None, title="数据日期"),
        market: Optional[str] = Query(None, title="市场类型"),
        industry: Optional[str] = Query(None, title="所属行业"),
        params: Paging = Depends(),
    ):
        super().__init__(params)
        self.data_date = data_date
        self.market = market
        self.industry = industry


class SyncRankingParams(BaseModel):
    """同步排行数据参数"""

    ranking_types: list[DailyRankingType] = Field(
        default_factory=lambda: [
            DailyRankingType.VOLUME,
            DailyRankingType.TURNOVER,
            DailyRankingType.AMOUNT,
        ],
        description="要同步的排行类型列表",
    )
    data_date: Optional[date] = Field(None, description="数据日期，默认今天")


class RankingSummaryParams(BaseModel):
    """排行榜单汇总查询参数"""

    ranking_type: DailyRankingType = Field(..., description="排行类型")
    data_date: Optional[date] = Field(None, description="数据日期，默认今天")
    top_n: int = Field(10, ge=1, le=100, description="获取前N名，默认10")
