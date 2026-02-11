#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/28
# @File           : stock_monitor_condition.py
# @IDE            : PyCharm
# @desc           : 股票监控配置查询参数-类依赖项

from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams


class StockMonitorConditionParams(QueryParams):
    """
    股票监控配置查询参数
    """

    def __init__(
            self,
            name: str | None = Query(None, title="监控名称/描述"),
            tag: str | None = Query(None, title="股票名称"),
            user_id: int | None = Query(None, title="创建用户ID"),
            is_active: int | None = Query(None, title="是否启用：1启用 0禁用"),
            owner: str | None = Query(None, title="拥有者"),
            reason: str | None = Query(None, title="条件原因"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.name = ("like", name) if name else None
        self.tag = tag
        self.user_id = user_id
        self.is_active = is_active
        self.owner = owner
        self.reason = reason
