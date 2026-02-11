#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/28
# @File           : stock_analysis.py
# @IDE            : PyCharm
# @desc           : 股票分析数据库 增删改查操作

from typing import Any
from sqlalchemy.orm.strategy_options import _AbstractLoad
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, delete, update
from apps.admin.stock import models, schemas
from datetime import datetime


class StockAnalysisDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(StockAnalysisDal, self).__init__()
        self.db = db
        self.model = models.StockAnalysis
        self.schema = schemas.StockAnalysisOut

    async def get_select_datas(self) -> list:
        """
        获取选择数据，全部数据
        :return:
        """
        sql = select(self.model)
        queryset = await self.db.scalars(sql)
        return [schemas.StockAnalysisOut.model_validate(i).model_dump() for i in queryset.all()]

    async def create_data(
            self,
            data: schemas.StockAnalysisCreate,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        """
        创建股票分析
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
            data: schemas.StockAnalysisUpdate,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        """
        更新单个股票分析
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
        删除多个股票分析
        :param ids: 数据集
        :param v_soft: 是否执行软删除
        :param kwargs: 其他更新字段
        """
        return await super(StockAnalysisDal, self).delete_datas(ids, v_soft, **kwargs)

    async def get_by_stock_code(self, stock_code: str, limit: int = 10) -> list:
        """
        根据股票代码获取分析列表
        :param stock_code: 股票代码
        :param limit: 限制数量
        :return: 分析列表
        """
        sql = select(self.model).where(self.model.stock_code == stock_code).order_by(
            self.model.analysis_time.desc()
        ).limit(limit)
        queryset = await self.db.scalars(sql)
        return [schemas.StockAnalysisOut.model_validate(i).model_dump() for i in queryset.all()]

    async def get_by_analysis_result(self, analysis_result: str) -> list:
        """
        根据分析结果获取列表
        :param analysis_result: 分析结果（看涨/看跌/中性）
        :return: 分析列表
        """
        sql = select(self.model).where(self.model.analysis_result == analysis_result).order_by(
            self.model.analysis_time.desc()
        )
        queryset = await self.db.scalars(sql)
        return [schemas.StockAnalysisOut.model_validate(i).model_dump() for i in queryset.all()]

    async def get_valid_analyses(self, is_valid: int = 1) -> list:
        """
        获取有效的分析记录
        :param is_valid: 是否有效
        :return: 分析列表
        """
        sql = select(self.model).where(self.model.is_valid == is_valid).order_by(
            self.model.analysis_time.desc()
        )
        queryset = await self.db.scalars(sql)
        return [schemas.StockAnalysisOut.model_validate(i).model_dump() for i in queryset.all()]

    async def verify_analysis(self, analysis_id: int, verification_result: str, is_valid: int = None) -> Any:
        """
        验证分析结果
        :param analysis_id: 分析ID
        :param verification_result: 验证结果（正确/错误/部分正确）
        :param is_valid: 是否有效（1有效 0无效）
        """
        update_dict = {
            "is_verified": 1,
            "verification_result": verification_result,
            "verification_date": datetime.now().date()
        }
        if is_valid is not None:
            update_dict["is_valid"] = is_valid

        update_data = schemas.StockAnalysisUpdate(**update_dict)
        return await self.put_data(analysis_id, update_data)

    async def update_send_status(self, analysis_id: int, is_send: int) -> None:
        """
        更新发送状态
        :param analysis_id: 分析ID
        :param is_send: 是否发送
        """
        await self.db.execute(
            update(self.model)
            .where(self.model.id == analysis_id)
            .values(is_send=is_send)
        )

    async def get_by_user_id(self, user_id: int) -> list:
        """
        根据用户ID获取分析列表
        :param user_id: 用户ID
        :return: 分析列表
        """
        sql = select(self.model).where(self.model.user_id == user_id).order_by(
            self.model.analysis_time.desc()
        )
        queryset = await self.db.scalars(sql)
        return [schemas.StockAnalysisOut.model_validate(i).model_dump() for i in queryset.all()]
