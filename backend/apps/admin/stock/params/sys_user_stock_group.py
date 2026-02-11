#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/02/08
# @File           : sys_user_stock_group.py
# @IDE            : PyCharm
# @desc           : 用户股票分组关联查询参数

from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams


class SysUserStockGroupParams(QueryParams):
    """
    用户股票分组关联查询参数
    """

    def __init__(
            self,
            user_id: int | None = Query(None, title="用户ID"),
            group_id: int | None = Query(None, title="分组ID"),
            stock_id: int | None = Query(None, title="股票ID"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.user_id = user_id
        self.group_id = group_id
        self.stock_id = stock_id
