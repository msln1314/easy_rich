#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/03/22
# @File           : review_crud.py
# @IDE            : PyCharm
# @desc           : 复盘记录数据库 增删改查操作

from datetime import date
from typing import Any, Optional, List
from sqlalchemy.orm.strategy_options import _AbstractLoad
from sqlalchemy import select
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from apps.admin.review import models, schemas


class ReviewDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(ReviewDal, self).__init__()
        self.db = db
        self.model = models.ReviewRecord
        self.schema = schemas.ReviewOut

    async def create_data(
        self,
        data: schemas.ReviewCreate,
        user_id: int,
        v_options: list[_AbstractLoad] = None,
        v_return_obj: bool = False,
        v_schema: Any = None,
    ) -> Any:
        """
        创建复盘记录
        :param data: 创建数据
        :param user_id: 用户ID
        :param v_options: 加载选项
        :param v_return_obj: 是否返回对象
        :param v_schema: 输出schema
        :return:
        """
        obj = self.model(**data.model_dump(), user_id=user_id)
        await self.flush(obj)
        return await self.out_dict(obj, v_options, v_return_obj, v_schema)

    async def put_data(
        self,
        data_id: int,
        data: schemas.ReviewUpdate,
        v_options: list[_AbstractLoad] = None,
        v_return_obj: bool = False,
        v_schema: Any = None,
    ) -> Any:
        """
        更新复盘记录
        :param data_id: 数据ID
        :param data: 更新数据
        :param v_options: 加载选项
        :param v_return_obj: 是否返回对象
        :param v_schema: 输出schema
        :return:
        """
        obj = await self.get_data(data_id, v_options=v_options)
        obj_dict = jsonable_encoder(data)
        for key, value in obj_dict.items():
            if value is not None:
                setattr(obj, key, value)
        await self.flush(obj)
        return await self.out_dict(obj, None, v_return_obj, v_schema)

    async def delete_datas(
        self, ids: list[int], v_soft: bool = False, **kwargs
    ) -> None:
        """
        删除复盘记录
        :param ids: 数据ID列表
        :param v_soft: 是否软删除
        :param kwargs: 其他参数
        """
        return await super(ReviewDal, self).delete_datas(ids, v_soft, **kwargs)

    async def get_by_user_id(
        self, user_id: int, review_type: Optional[str] = None, limit: int = 20
    ) -> list:
        """
        根据用户ID获取复盘记录列表
        :param user_id: 用户ID
        :param review_type: 复盘类型过滤
        :param limit: 返回数量限制
        :return: 复盘记录列表
        """
        sql = select(self.model).where(self.model.user_id == user_id)
        if review_type:
            sql = sql.where(self.model.review_type == review_type)
        sql = sql.order_by(self.model.review_date.desc()).limit(limit)
        queryset = await self.db.scalars(sql)
        return [
            schemas.ReviewOut.model_validate(i).model_dump() for i in queryset.all()
        ]

    async def get_by_portfolio_id(self, portfolio_id: int) -> list:
        """
        根据组合ID获取复盘记录列表
        :param portfolio_id: 组合ID
        :return: 复盘记录列表
        """
        sql = select(self.model).where(self.model.portfolio_id == portfolio_id)
        sql = sql.order_by(self.model.review_date.desc())
        queryset = await self.db.scalars(sql)
        return [
            schemas.ReviewOut.model_validate(i).model_dump() for i in queryset.all()
        ]

    async def get_by_date_range(
        self,
        user_id: int,
        start_date: date,
        end_date: date,
        review_type: Optional[str] = None,
    ) -> list:
        """
        根据日期范围获取复盘记录
        :param user_id: 用户ID
        :param start_date: 开始日期
        :param end_date: 结束日期
        :param review_type: 复盘类型过滤
        :return: 复盘记录列表
        """
        sql = select(self.model).where(
            self.model.user_id == user_id,
            self.model.review_date >= start_date,
            self.model.review_date <= end_date,
        )
        if review_type:
            sql = sql.where(self.model.review_type == review_type)
        sql = sql.order_by(self.model.review_date.desc())
        queryset = await self.db.scalars(sql)
        return [
            schemas.ReviewOut.model_validate(i).model_dump() for i in queryset.all()
        ]

    async def get_latest_by_type(
        self, user_id: int, review_type: str
    ) -> Optional[dict]:
        """
        获取用户指定类型的最新复盘记录
        :param user_id: 用户ID
        :param review_type: 复盘类型
        :return: 最新复盘记录
        """
        sql = (
            select(self.model)
            .where(self.model.user_id == user_id, self.model.review_type == review_type)
            .order_by(self.model.review_date.desc())
            .limit(1)
        )
        queryset = await self.db.scalars(sql)
        result = queryset.first()
        if result:
            return schemas.ReviewOut.model_validate(result).model_dump()
        return None
