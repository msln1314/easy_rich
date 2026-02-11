#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:19
# @File           : task.py
# @IDE            : PyCharm
# @desc           : 查询参数-类依赖项

"""
类依赖项-官方文档：https://fastapi.tiangolo.com/zh/tutorial/dependencies/classes-as-dependencies/
"""
from fastapi import Depends
from core.dependencies import Paging, QueryParams


class TaskLogParams(QueryParams):
    """
    任务日志查询参数
    """
    def __init__(
        self,
        job_id: int = None,
        job_name: str = None,
        params: Paging = Depends()
    ):
        super().__init__(params)
        self.job_id = job_id
        self.job_name = ("like", job_name)
        self.v_order = "desc"
        self.v_order_field = "created_at"
