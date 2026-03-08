#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version : 1.0
# @Create Time : 2025/02/15
# @File : stock_monitor_log.py
# @IDE : PyCharm
# @desc : 股票监听推送日志查询参数

from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams
from datetime import datetime


class StockMonitorLogParams(QueryParams):
    """股票监听日志查询参数"""

    def __init__(
        self,
        strategy_id: int | None = Query(None, title="策略ID"),
        stock_code: str | None = Query(None, title="股票代码"),
        stock_name: str | None = Query(None, title="股票名称"),
        user_id: int | None = Query(None, title="用户ID"),
        strategy_type: str | None = Query(None, title="监听策略类型"),
        notify_status: int | None = Query(None, title="推送状态：0待推送 1成功 2失败"),
        notify_method: str | None = Query(None, title="推送方式"),
        start_time: datetime | None = Query(None, title="开始时间"),
        end_time: datetime | None = Query(None, title="结束时间"),
        params: Paging = Depends(),
    ):
        super().__init__(params)
        self.strategy_id = strategy_id
        self.stock_code = stock_code
        self.stock_name = ("like", stock_name) if stock_name else None
        self.user_id = user_id
        self.strategy_type = strategy_type
        self.notify_status = notify_status
        self.notify_method = notify_method
        self.start_time = start_time
        self.end_time = end_time
