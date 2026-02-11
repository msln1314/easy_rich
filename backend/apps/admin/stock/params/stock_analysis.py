#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/28
# @File           : stock_analysis.py
# @IDE            : PyCharm
# @desc           : 股票分析查询参数-类依赖项

from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams


class StockAnalysisParams(QueryParams):
    """
    股票分析查询参数
    """

    def __init__(
            self,
            stock_code: str | None = Query(None, title="股票代码"),
            stock_name: str | None = Query(None, title="股票名称"),
            stock_industry: str | None = Query(None, title="股票行业"),
            analysis_result: str | None = Query(None, title="分析结果：看涨/看跌/中性"),
            analysis_type: str | None = Query(None, title="分析类型"),
            analysis_period: str | None = Query(None, title="分析周期"),
            risk_level: str | None = Query(None, title="风险等级"),
            analysis_source: str | None = Query(None, title="分析来源"),
            is_valid: int | None = Query(None, title="是否有效"),
            is_verified: int | None = Query(None, title="是否已验证"),
            is_send: int | None = Query(None, title="是否发送"),
            user_id: int | None = Query(None, title="用户ID"),
            tags: str | None = Query(None, title="标签"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.stock_code = stock_code
        self.stock_name = ("like", stock_name) if stock_name else None
        self.stock_industry = stock_industry
        self.analysis_result = analysis_result
        self.analysis_type = analysis_type
        self.analysis_period = analysis_period
        self.risk_level = risk_level
        self.analysis_source = analysis_source
        self.is_valid = is_valid
        self.is_verified = is_verified
        self.is_send = is_send
        self.user_id = user_id
        self.tags = ("like", tags) if tags else None
