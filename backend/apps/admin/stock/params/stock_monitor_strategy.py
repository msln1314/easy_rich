#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version : 1.0
# @Create Time : 2025/02/15
# @File : stock_monitor_strategy.py
# @IDE : PyCharm
# @desc : 股票监听策略查询参数

from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams


class StockMonitorStrategyParams(QueryParams):
    """股票监听策略查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, title="监听策略名称"),
        tag: str | None = Query(None, title="标签"),
        stock_code: str | None = Query(None, title="股票代码"),
        stock_name: str | None = Query(None, title="股票名称"),
        user_id: int | None = Query(None, title="创建用户ID"),
        is_active: int | None = Query(None, title="是否启用：1启用 0禁用"),
        strategy_type: str | None = Query(None, title="监听策略类型"),
        priority: int | None = Query(None, title="优先级：1高 2中 3低"),
        reason: str | None = Query(None, title="监听原因"),
        notify_enabled: int | None = Query(None, title="是否启用推送"),
        params: Paging = Depends(),
    ):
        super().__init__(params)
        self.name = ("like", name) if name else None
        self.tag = tag
        self.stock_code = stock_code
        self.stock_name = ("like", stock_name) if stock_name else None
        self.user_id = user_id
        self.is_active = is_active
        self.strategy_type = strategy_type
        self.priority = priority
        self.reason = ("like", reason) if reason else None
        self.notify_enabled = notify_enabled
