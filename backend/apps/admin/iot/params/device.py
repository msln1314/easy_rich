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


class DeviceParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            # name: str | None = Query(None, title="名称"),
            mac: str | None = Query(None, title="mac"),
            keywords: str | None = Query(None, title="关联查询"),
            ip: str | None = Query(None, title="ip"),
            address: str | None = Query(None, title="address"),
            area: str | None = Query(None, title="area"),
            device_type: str | None = Query(None, title=""),
            online_status: str | None = Query(None, title="在线状态"),
            product_id: int | None = Query(None, title="名称"),
            is_active: bool | None = Query(None, title="是否可用"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        # self.name = ("like", name)
        self.mac = ("like", mac)
        self.ip = ("like", ip)
        self.address = ("like", address)
        self.area = ("like", area)
        self.online_status = online_status
        self.keywords = keywords
        self.is_active = is_active
        self.product_id = product_id
        self.device_type = device_type



