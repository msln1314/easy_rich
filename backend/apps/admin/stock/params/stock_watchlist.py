#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/28
# @File           : stock_watchlist.py
# @IDE            : PyCharm
# @desc           : 股票关注列表查询参数-类依赖项

from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams


class StockWatchlistParams(QueryParams):
    """
    股票关注列表查询参数
    """

    def __init__(
            self,
            stock_code: str | None = Query(None, title="股票代码"),
            stock_name: str | None = Query(None, title="股票名称"),
            user_id: int | None = Query(None, title="用户ID"),
            category: str | None = Query(None, title="关注分类"),
            tags: str | None = Query(None, title="标签"),
            is_active: int | None = Query(None, title="是否关注：1关注中 0已取消"),
            priority: int | None = Query(None, title="关注优先级"),
            is_analyze: int | None = Query(None, title="是否已分析"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.stock_code = stock_code
        self.stock_name = ("like", stock_name) if stock_name else None
        self.user_id = user_id
        self.category = category
        self.tags = ("like", tags) if tags else None
        self.is_active = is_active
        self.priority = priority
        self.is_analyze = is_analyze
