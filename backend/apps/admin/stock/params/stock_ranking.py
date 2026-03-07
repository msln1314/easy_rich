#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/1
# @File           : stock_ranking.py
# @IDE            : PyCharm
# @desc           : 个股排行查询参数

from enum import Enum
from fastapi import Query, Depends
from core.dependencies import Paging, QueryParams
from pydantic import BaseModel, Field


class RankingType(str, Enum):
    """排行类型"""
    TURNOVER = "turnover"  # 换手率
    AMOUNT = "amount"  # 资金量
    VOLUME_RATIO = "volume_ratio"  # 量比
    CHANGE_PERCENT = "change_percent"  # 涨跌幅
    MARKET_CAP = "market_cap"  # 市值
    AMPLITUDE = "amplitude"  # 振幅


class RankingOrder(str, Enum):
    """排序方向"""
    DESC = "desc"  # 降序
    ASC = "asc"  # 升序


class StockRankingParams(QueryParams):
    """
    个股排行查询参数
    """

    def __init__(
        self,
        ranking_type: RankingType = Query(RankingType.TURNOVER, title="排行类型"),
        order: RankingOrder = Query(RankingOrder.DESC, title="排序方向"),
        industry: str | None = Query(None, title="所属行业"),
        market: str | None = Query(None, title="市场类型"),
        stock_code: str | None = Query(None, title="股票代码"),
        stock_name: str | None = Query(None, title="股票名称"),
        params: Paging = Depends()
    ):
        super().__init__(params)
        self.ranking_type = ranking_type
        self.order = order
        self.industry = industry
        self.market = market
        self.stock_code = stock_code
        self.stock_name = ("like", stock_name) if stock_name else None

    def get_sort_field(self):
        """根据排行类型获取排序字段"""
        field_map = {
            RankingType.TURNOVER: StockBasicInfo.turnover_rate,
            RankingType.AMOUNT: StockBasicInfo.amount,
            RankingType.VOLUME_RATIO: StockBasicInfo.volume_ratio,
            RankingType.CHANGE_PERCENT: StockBasicInfo.change_percent,
            RankingType.MARKET_CAP: StockBasicInfo.total_market_cap,
            RankingType.AMPLITUDE: StockBasicInfo.amplitude,
        }
        return field_map.get(self.ranking_type)


# 避免循环导入，放在文件末尾
from apps.admin.stock.models.stock_basic_info import StockBasicInfo
