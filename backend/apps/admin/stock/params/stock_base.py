#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:19
# @File           : user.py
# @IDE            : PyCharm
# @desc           : 查询参数-类依赖项

"""
类依赖项-官方文档：https://fastapi.tiangolo.com/zh/tutorial/dependencies/classes-as-dependencies/
"""
from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams
from pydantic import BaseModel, Field

class StockBaseInfoParams(QueryParams):
    """
    股票基本信息查询参数
    """

    def __init__(
            self,
            full_code: str | None = Query(None, title="TS 股票代码"),
            stock_code: str | None = Query(None, title="股票代码"),
            name: str | None = Query(None, title="股票名称"),
            keywords: str | None = Query(None, title="关键词"),
            area: str | None = Query(None, title="地域"),
            industry: str | None = Query(None, title="所属行业"),
            market: str | None = Query(None, title="市场类型"),
            is_hs: str | None = Query(None, title="是否沪深港通标的"),
            status: str | None = Query(None, title="上市状态"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.full_code = full_code
        self.stock_code = stock_code
        self.name = ("like", name) if name else None
        self.area = ("like", area) if area else None
        self.industry = industry
        self.market = market
        self.is_hs = is_hs
        self.status = status
        self.keywords = keywords




class StockParams(BaseModel):
    stock_code: str = Field(..., title="股票代码")

class HistoricalParams(BaseModel):
    stock_code: str = Field(..., title="股票代码")
    start_date: str | None = Field(None, title="开始日期")
    end_date: str | None = Field(None, title="结束日期")
