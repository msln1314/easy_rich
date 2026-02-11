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


class ProductParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            name: str | None = Query(None, title="名称"),
            product_type: str | None = Query(None, title="产品类型"),
            product_tag: str | None = Query(None, title="产品标签"),
            # is_active: bool | None = Query(None, title="是否可用"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.name = ("like", name)
        self.product_tag = product_tag
        self.product_type = product_type
