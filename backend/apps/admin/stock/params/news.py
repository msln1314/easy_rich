#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/28
# @File           : news.py
# @IDE            : PyCharm
# @desc           : 新闻信息查询参数-类依赖项

from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams


class NewsParams(QueryParams):
    """
    新闻信息查询参数
    """

    def __init__(
            self,
            name: str | None = Query(None, title="新闻标题"),
            data_from: str | None = Query(None, title="数据来源"),
            tag: str | None = Query(None, title="标签"),
            is_send: int | None = Query(None, title="是否发送"),
            priority: int | None = Query(None, title="优先级"),
            category: str | None = Query(None, title="板块"),
            is_analyze: int | None = Query(None, title="是否分析"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.name = ("like", name) if name else None
        self.data_from = data_from
        self.tag = tag
        self.is_send = is_send
        self.priority = priority
        self.category = category
        self.is_analyze = is_analyze
