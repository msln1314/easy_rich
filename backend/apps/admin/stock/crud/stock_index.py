#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/10
# @File           : stock_index.py
# @IDE            : PyCharm
# @desc           : 大盘指数 增删改查操作

from typing import Any, Optional
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date
from apps.admin.stock import models, schemas


class StockIndexDal(DalBase):
    """大盘指数 DalBase 操作类"""

    def __init__(self, db: AsyncSession):
        super(StockIndexDal, self).__init__()
        self.db = db
        self.model = models.StockIndex
        self.schema = schemas.StockIndexOut

    async def get_latest_by_code(self, index_code: str) -> Optional[Any]:
        """
        获取指数最新行情

        Args:
            index_code: 指数代码

        Returns:
            最新行情数据
        """
        query = (
            select(self.model)
            .filter(self.model.index_code == index_code)
            .order_by(self.model.data_date.desc())
            .limit(1)
        )
        datas = await self.get_datas(query=query)
        return datas[0] if datas else None

    async def get_latest_quotes(self, index_codes: list[str]) -> list:
        """
        获取多个指数的最新行情

        Args:
            index_codes: 指数代码列表

        Returns:
            指数行情列表
        """
        query = select(self.model).filter(
            self.model.index_code.in_(index_codes)
        )
        query = query.order_by(self.model.index_code, self.model.data_date.desc())
        datas = await self.get_datas(query=query)

        # 去重，每个指数只取最新
        seen = set()
        result = []
        for d in datas:
            if d.index_code not in seen:
                seen.add(d.index_code)
                result.append(d)
        return result

    async def get_history_by_code(
        self,
        index_code: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> list:
        """
        获取指数历史数据

        Args:
            index_code: 指数代码
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            历史数据列表
        """
        query = select(self.model).filter(
            self.model.index_code == index_code,
        )
        if start_date:
            query = query.filter(self.model.data_date >= start_date)
        if end_date:
            query = query.filter(self.model.data_date <= end_date)

        query = query.order_by(self.model.data_date)

        return await self.get_datas(query=query)

    async def batch_create_datas(
        self, datas: list[dict], v_return_obj: bool = False
    ) -> list:
        """
        批量创建数据

        Args:
            datas: 数据列表
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