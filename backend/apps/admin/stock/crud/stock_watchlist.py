#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/28
# @File           : stock_watchlist.py
# @IDE            : PyCharm
# @desc           : 股票关注列表数据库 增删改查操作

from typing import Any
from sqlalchemy.orm.strategy_options import _AbstractLoad
from core.crud import DalBase
from utils.excel.excel_manage import ExcelManage
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, delete, update
from apps.admin.stock import models, schemas, params


class StockWatchlistDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(StockWatchlistDal, self).__init__()
        self.db = db
        self.model = models.StockWatchlist
        self.schema = schemas.StockWatchlistOut

    async def get_select_datas(self) -> list:
        """
        获取选择数据，全部数据
        :return:
        """
        sql = select(self.model)
        queryset = await self.db.scalars(sql)
        return [schemas.StockWatchlistOut.model_validate(i).model_dump() for i in queryset.all()]

    async def create_data(
            self,
            data: schemas.StockWatchlistCreate,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        """
        创建股票关注列表
        :param data:
        :param v_options:
        :param v_return_obj:
        :param v_schema:
        :return:
        """
        obj = self.model(**data.model_dump())
        await self.flush(obj)
        return await self.out_dict(obj, v_options, v_return_obj, v_schema)

    async def put_data(
            self,
            data_id: int,
            data: schemas.StockWatchlistUpdate,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        """
        更新单个股票关注列表
        :param data_id:
        :param data:
        :param v_options:
        :param v_return_obj:
        :param v_schema:
        :return:
        """
        obj = await self.get_data(data_id, v_options=v_options)
        obj_dict = jsonable_encoder(data)
        for key, value in obj_dict.items():
            setattr(obj, key, value)
        await self.flush(obj)
        return await self.out_dict(obj, None, v_return_obj, v_schema)

    async def delete_datas(self, ids: list[int], v_soft: bool = False, **kwargs) -> None:
        """
        删除多个股票关注列表
        :param ids: 数据集
        :param v_soft: 是否执行软删除
        :param kwargs: 其他更新字段
        """
        return await super(StockWatchlistDal, self).delete_datas(ids, v_soft, **kwargs)

    async def get_by_user_id(self, user_id: int, is_active: int = 1) -> list:
        """
        根据用户ID获取关注列表
        :param user_id: 用户ID
        :param is_active: 是否关注中
        :return: 关注列表
        """
        sql = select(self.model).where(
            self.model.user_id == user_id,
            self.model.is_active == is_active
        ).order_by(
            self.model.priority.asc(),
            self.model.created_at.desc()
        )
        queryset = await self.db.scalars(sql)
        return [schemas.StockWatchlistOut.model_validate(i).model_dump() for i in queryset.all()]

    async def get_by_user_and_stock(self, user_id: int, stock_code: str) -> Any:
        """
        根据用户ID和股票代码获取关注记录
        :param user_id: 用户ID
        :param stock_code: 股票代码
        :return: 关注记录
        """
        sql = select(self.model).where(
            self.model.user_id == user_id,
            self.model.stock_code == stock_code
        ).order_by(self.model.date_at.desc())
        result = await self.db.execute(sql)
        return result.scalar_one_or_none()

    async def cancel_follow(self, user_id: int, stock_code: str) -> None:
        """
        取消关注
        :param user_id: 用户ID
        :param stock_code: 股票代码
        """
        await self.db.execute(
            update(self.model)
            .where(
                self.model.user_id == user_id,
                self.model.stock_code == stock_code,
                self.model.is_active == 1
            )
            .values(is_active=0)
        )

    async def update_watch_stats(self, data_id: int, stats_data: dict) -> None:
        """
        更新关注统计数据
        :param data_id: 记录ID
        :param stats_data: 统计数据
        """
        await self.db.execute(
            update(self.model)
            .where(self.model.id == data_id)
            .values(**stats_data)
        )

    async def get_active_watchlist_by_user(self, user_id: int) -> list:
        """
        获取用户的所有活跃关注记录
        :param user_id: 用户ID
        :return: 关注列表
        """
        sql = select(self.model).where(
            self.model.user_id == user_id,
            self.model.is_active == 1
        )
        queryset = await self.db.scalars(sql)
        return [schemas.StockWatchlistOut.model_validate(i).model_dump() for i in queryset.all()]

    async def export_query_list(self, header: list, params: params.StockWatchlistParams) -> dict:
        """
        导出股票关注查询列表为 excel
        :param header: 表头字段
        :param params: 查询参数
        :return: 导出文件信息
        """
        params.limit = 1000000
        datas = await self.get_datas(**params.dict(), v_return_objs=True)

        # 获取表头
        row = list(map(lambda i: i.get("label"), header))
        rows = []

        # 优先级映射
        priority_map = {1: '高', 2: '中', 3: '低'}

        for watchlist in datas:
            data = []
            for item in header:
                field = item.get("field")
                # 通过反射获取对应的属性值
                value = getattr(watchlist, field, "")

                # 特殊字段处理
                if field == "priority":
                    value = priority_map.get(value, value)
                elif field == "is_active":
                    value = "关注中" if value == 1 else "已取消"
                elif field == "is_analyze":
                    value = "已分析" if value == 1 else "未分析"

                data.append(value)
            rows.append(data)

        em = ExcelManage()
        em.create_excel("股票关注列表")
        em.write_list(rows, row)
        file_url = em.save_excel()
        em.close()
        return {"url": file_url, "filename": "股票关注列表.xlsx"}
