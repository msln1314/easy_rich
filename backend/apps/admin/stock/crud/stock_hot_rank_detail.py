#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/9
# @File           : stock_hot_rank_detail.py
# @IDE            : PyCharm
# @desc           : 股票热度详情 增删改查操作

from typing import Any, Optional
from sqlalchemy.orm.strategy_options import _AbstractLoad
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date
from apps.admin.stock import models


class StockHotRankDetailDal(DalBase):
    """股票热度详情 DalBase 操作类"""

    def __init__(self, db: AsyncSession):
        super(StockHotRankDetailDal, self).__init__()
        self.db = db
        self.model = models.StockHotRankDetail

    async def create_data(
        self,
        data: dict,
        v_options: list[_AbstractLoad] = None,
        v_return_obj: bool = False,
        v_schema: Any = None,
    ) -> Any:
        """
        创建热度详情数据

        Args:
            data: 热度详情数据
            v_options: 加载选项
            v_return_obj: 是否返回对象
            v_schema: 自定义输出Schema
        """
        obj = self.model(**data)
        await self.flush(obj)
        return await self.out_dict(obj, v_options, v_return_obj, v_schema)

    async def batch_create_datas(
        self, datas: list[dict], v_return_obj: bool = False
    ) -> list:
        """
        批量创建热度详情数据

        Args:
            datas: 热度详情数据列表
            v_return_obj: 是否返回对象

        Returns:
            创建的数据列表
        """
        objs = [self.model(**data) for data in datas]
        self.db.add_all(objs)
        await self.flush(*objs)
        if v_return_obj:
            return objs
        return await self.out_dict(objs)

    async def get_details_by_stock(
        self,
        stock_code: str,
        start_date: Optional[date] = None,
    ) -> list:
        """
        获取指定股票的历史热度详情

        Args:
            stock_code: 股票代码
            start_date: 开始日期

        Returns:
            热度详情列表
        """
        filters = [self.model.stock_code == stock_code]
        if start_date:
            filters.append(self.model.data_date >= start_date)

        query = select(self.model).filter(*filters).order_by(self.model.data_date)

        return await self.get_datas(query=query)