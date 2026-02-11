#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/02/08
# @File           : stock_group.py
# @IDE            : PyCharm
# @desc           : 股票分组查询参数

from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams


class StockGroupParams(QueryParams):
    """
    股票分组查询参数
    """

    def __init__(
            self,
            name: str | None = Query(None, title="分组名称"),
            status: int | None = Query(None, title="是否禁用"),
            user_id: int | None = Query(None, title="用户ID"),
            parent_id: int | None = Query(None, title="上级分组ID"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.name = name
        self.status = status
        self.user_id = user_id
        self.parent_id = parent_id
