#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/9
# @File           : stock_daily_ranking.py
# @IDE            : PyCharm
# @desc           : 个股每日排行数据 增删改查操作

from typing import Any, Optional
from sqlalchemy.orm.strategy_options import _AbstractLoad
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, func
from datetime import date
from apps.admin.stock import models, schemas


class StockDailyRankingDal(DalBase):
    """个股每日排行数据 DalBase 操作类"""

    def __init__(self, db: AsyncSession):
        super(StockDailyRankingDal, self).__init__()
        self.db = db
        self.model = models.StockDailyRanking
        self.schema = schemas.StockDailyRankingOut

    async def create_data(
        self,
        data: dict,
        v_options: list[_AbstractLoad] = None,
        v_return_obj: bool = False,
        v_schema: Any = None,
    ) -> Any:
        """
        创建每日排行数据

        Args:
            data: 排行数据
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
        批量创建每日排行数据

        Args:
            datas: 排行数据列表
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

    async def put_data(
        self,
        data_id: int,
        data: dict,
        v_options: list[_AbstractLoad] = None,
        v_return_obj: bool = False,
        v_schema: Any = None,
    ) -> Any:
        """
        更新单个每日排行数据

        Args:
            data_id: 数据ID
            data: 更新的数据
            v_options: 加载选项
            v_return_obj: 是否返回对象
            v_schema: 自定义输出Schema
        """
        obj = await self.get_data(data_id, v_options=v_options)
        for key, value in data.items():
            if value is not None:
                setattr(obj, key, value)
        await self.flush(obj)
        return await self.out_dict(obj, None, v_return_obj, v_schema)

    async def delete_datas(
        self, ids: list[int], v_soft: bool = False, **kwargs
    ) -> None:
        """
        删除多个每日排行数据

        Args:
            ids: 数据ID列表
            v_soft: 是否执行软删除
            kwargs: 其他更新字段
        """
        return await super(StockDailyRankingDal, self).delete_datas(
            ids, v_soft, **kwargs
        )

    async def get_ranking_by_date_and_type(
        self,
        data_date: date,
        ranking_type: str,
        industry: Optional[str] = None,
        market: Optional[str] = None,
        stock_code: Optional[str] = None,
        stock_name: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list, int]:
        """
        根据日期和排行类型获取排行数据

        Args:
            data_date: 数据日期
            ranking_type: 排行类型
            industry: 所属行业
            market: 市场类型
            stock_code: 股票代码
            stock_name: 股票名称
            page: 页码
            page_size: 每页数量

        Returns:
            (数据列表, 总数)
        """
        filters = [
            self.model.data_date == data_date,
            self.model.ranking_type == ranking_type,
        ]
        if industry:
            filters.append(self.model.industry == industry)
        if market:
            filters.append(self.model.market == market)
        if stock_code:
            filters.append(self.model.stock_code == stock_code)
        if stock_name:
            filters.append(self.model.stock_name.like(f"%{stock_name}%"))

        # 获取总数
        total = await self.get_count(v_where=filters)

        # 分页查询
        query = select(self.model).filter(*filters).order_by(self.model.rank)
        query = query.offset((page - 1) * page_size).limit(page_size)

        datas = await self.get_datas(query=query)

        return datas, total

    async def get_ranking_by_stock(
        self,
        stock_code: str,
        ranking_type: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> list:
        """
        获取指定股票的排行趋势

        Args:
            stock_code: 股票代码
            ranking_type: 排行类型
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            排行趋势数据列表
        """
        filters = [
            self.model.stock_code == stock_code,
            self.model.ranking_type == ranking_type,
        ]
        if start_date:
            filters.append(self.model.data_date >= start_date)
        if end_date:
            filters.append(self.model.data_date <= end_date)

        query = select(self.model).filter(*filters).order_by(self.model.data_date)

        return await self.get_datas(query=query)

    async def get_ranking_summary(
        self,
        data_date: date,
        ranking_type: str,
        top_n: int = 10,
    ) -> tuple[list, int]:
        """
        获取排行榜单汇总（TOP N）

        Args:
            data_date: 数据日期
            ranking_type: 排行类型
            top_n: 获取前N名

        Returns:
            (TOP N数据列表, 当日上榜总数)
        """
        filters = [
            self.model.data_date == data_date,
            self.model.ranking_type == ranking_type,
        ]

        # 获取当日上榜总数
        total = await self.get_count(v_where=filters)

        # 获取TOP N数据
        query = (
            select(self.model)
            .filter(*filters)
            .order_by(self.model.rank)
            .limit(top_n)
        )
        rankings = await self.get_datas(query=query)

        return rankings, total

    async def get_distinct_industries(self, ranking_type: str) -> list:
        """
        获取指定排行类型关联的行业列表

        Args:
            ranking_type: 排行类型

        Returns:
            行业列表
        """
        query = (
            select(self.model.industry)
            .filter(
                self.model.ranking_type == ranking_type,
                self.model.industry.isnot(None),
            )
            .distinct()
        )
        result = await self.execute_query(query)
        industries = result.scalars().all()
        return sorted([ind for ind in industries if ind])