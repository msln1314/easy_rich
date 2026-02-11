#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/28
# @File           : stock_monitor_condition.py
# @IDE            : PyCharm
# @desc           : 股票监控配置数据库 增删改查操作

from typing import Any
from sqlalchemy.orm.strategy_options import _AbstractLoad
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, delete, update
from apps.admin.stock import models, schemas


class StockMonitorConditionDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(StockMonitorConditionDal, self).__init__()
        self.db = db
        self.model = models.StockMonitorCondition
        self.schema = schemas.StockMonitorConditionOut

    async def get_select_datas(self) -> list:
        """
        获取选择数据，全部数据
        :return:
        """
        sql = select(self.model)
        queryset = await self.db.scalars(sql)
        return [schemas.StockMonitorConditionOut.model_validate(i).model_dump() for i in queryset.all()]

    async def create_data(
            self,
            data: schemas.StockMonitorConditionCreate,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        """
        创建股票监控配置
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
            data: schemas.StockMonitorConditionUpdate,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        """
        更新单个股票监控配置
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
        删除多个股票监控配置
        :param ids: 数据集
        :param v_soft: 是否执行软删除
        :param kwargs: 其他更新字段
        """
        return await super(StockMonitorConditionDal, self).delete_datas(ids, v_soft, **kwargs)

    async def get_active_conditions(self, user_id: int = None) -> list:
        """
        获取启用的监控条件
        :param user_id: 用户ID，None表示获取所有用户的
        :return: 监控条件列表
        """
        sql = select(self.model).where(self.model.is_active == 1)
        if user_id:
            sql = sql.where(self.model.user_id == user_id)
        queryset = await self.db.scalars(sql)
        return [schemas.StockMonitorConditionOut.model_validate(i).model_dump() for i in queryset.all()]

    async def update_active_status(self, condition_id: int, is_active: int) -> None:
        """
        更新监控条件的启用状态
        :param condition_id: 条件ID
        :param is_active: 是否启用
        """
        await self.db.execute(
            update(self.model)
            .where(self.model.id == condition_id)
            .values(is_active=is_active)
        )

    async def get_by_user_id(self, user_id: int) -> list:
        """
        根据用户ID获取监控条件列表
        :param user_id: 用户ID
        :return: 监控条件列表
        """
        sql = select(self.model).where(self.model.user_id == user_id).order_by(
            self.model.created_at.desc()
        )
        queryset = await self.db.scalars(sql)
        return [schemas.StockMonitorConditionOut.model_validate(i).model_dump() for i in queryset.all()]
