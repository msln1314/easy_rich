#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/9
# @File           : stock_hot_rank.py
# @IDE            : PyCharm
# @desc           : 股票热度排行 增删改查操作

from typing import Any, Optional
from sqlalchemy.orm.strategy_options import _AbstractLoad
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date
from apps.admin.stock import models, schemas


class StockHotRankDal(DalBase):
    """股票热度排行 DalBase 操作类"""

    def __init__(self, db: AsyncSession):
        super(StockHotRankDal, self).__init__()
        self.db = db
        self.model = models.StockHotRank
        self.schema = schemas.HotRankingOut

    async def create_data(
        self,
        data: dict,
        v_options: list[_AbstractLoad] = None,
        v_return_obj: bool = False,
        v_schema: Any = None,
    ) -> Any:
        """
        创建热度排行数据

        Args:
            data: 热度排行数据
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
        批量创建热度排行数据

        Args:
            datas: 热度排行数据列表
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

    async def get_hot_rank_by_date(
        self,
        data_date: date,
        market: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list, int]:
        """
        根据日期获取热度排行数据

        Args:
            data_date: 数据日期
            market: 市场类型
            page: 页码
            page_size: 每页数量

        Returns:
            (数据列表, 总数)
        """
        filters = [self.model.data_date == data_date]
        if market:
            filters.append(self.model.market == market)

        # 获取总数
        total = await self.get_count(v_where=filters)

        # 分页查询
        query = select(self.model).filter(*filters).order_by(self.model.rank)
        query = query.offset((page - 1) * page_size).limit(page_size)

        datas = await self.get_datas(query=query)

        return datas, total