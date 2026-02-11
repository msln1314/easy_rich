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


class ClientParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            name: str | None = Query(None, title="名称"),
            keywords: str | None = Query(None, title="ip"),
            address: str | None = Query(None, title="address"),
            area: str | None = Query(None, title="area"),
            client_type: str | None = Query(None, title="客户端类型"),
            port_status: int | None = Query(None, title="端口状态"),
            online_status: str | None = Query(None, title="在线状态"),
            bind_status: int | None = Query(None, title="绑定状态"),
            group_id: int | None = Query(None, title="名称"),
            is_active: bool | None = Query(None, title="是否可用"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.name = name
        # self.sn = ("like", name)
        # self.ip = ("like", keywords)
        self.keywords = keywords
        self.is_active = is_active
        self.group_id = group_id
        self.client_type = client_type
        self.port_status = port_status
        self.online_status = online_status
        self.bind_status = bind_status
        self.address = ("like", address)
        self.area = ("like", area)



