#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:18
# @File           : stock_base_info.py
# @IDE            : PyCharm
# @desc           : 股票基本信息数据库 增删改查操作

from typing import Any
from sqlalchemy.orm.strategy_options import _AbstractLoad
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, delete, update
from datetime import datetime
from apps.admin.stock import models, schemas


class StockBaseInfoDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(StockBaseInfoDal, self).__init__()
        self.db = db
        self.model = models.StockBasicInfo
        self.schema = schemas.StockBaseInfoOut

    async def get_select_datas(self) -> list:
        """
        获取选择数据，全部数据
        :return:
        """
        sql = select(self.model)
        queryset = await self.db.scalars(sql)
        return [schemas.StockBaseInfoOut.model_validate(i).model_dump() for i in queryset.all()]

    async def create_data(
            self,
            data: schemas.StockBaseInfoCreate,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        """
        创建股票基本信息
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
            data: schemas.StockBaseInfoUpdate,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        """
        更新单个股票基本信息
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
        删除多个股票基本信息
        :param ids: 数据集
        :param v_soft: 是否执行软删除
        :param kwargs: 其他更新字段
        """
        return await super(StockBaseInfoDal, self).delete_datas(ids, v_soft, **kwargs)

 


    async def batch_delete_by_full_codes(self, full_codes: list[str]) -> None:
        """
        根据full_code批量删除股票
        :param full_codes: full_code列表
        """
        await self.db.execute(
            delete(self.model).where(self.model.full_code.in_(full_codes))
        )







