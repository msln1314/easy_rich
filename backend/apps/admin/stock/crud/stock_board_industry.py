#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/31
# @File           : stock_board_industry.py
# @IDE            : PyCharm
# @desc           : 股票行业板块数据库 增删改查操作

from typing import Any
from sqlalchemy.orm.strategy_options import _AbstractLoad
from core.crud import DalBase
from utils.excel.excel_manage import ExcelManage
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, delete, update, or_, and_
from apps.admin.stock import models, schemas, params


class StockBoardIndustryDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(StockBoardIndustryDal, self).__init__()
        self.db = db
        self.model = models.StockBoardIndustry
        self.schema = schemas.StockBoardIndustryOut

    async def get_select_datas(self) -> list:
        """
        获取选择数据，全部数据
        :return:
        """
        sql = select(self.model)
        queryset = await self.db.scalars(sql)
        return [
            schemas.StockBoardIndustryOut.model_validate(i).model_dump()
            for i in queryset.all()
        ]

    async def create_data(
        self,
        data: schemas.StockBoardIndustryCreate,
        v_options: list[_AbstractLoad] = None,
        v_return_obj: bool = False,
        v_schema: Any = None,
    ) -> Any:
        """
        创建股票行业板块
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
        data: schemas.StockBoardIndustryUpdate,
        v_options: list[_AbstractLoad] = None,
        v_return_obj: bool = False,
        v_schema: Any = None,
    ) -> Any:
        """
        更新单个股票行业板块
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

    async def delete_datas(
        self, ids: list[int], v_soft: bool = False, **kwargs
    ) -> None:
        """
        删除多个股票行业板块
        :param ids: 数据集
        :param v_soft: 是否执行软删除
        :param kwargs: 其他更新字段
        """
        return await super(StockBoardIndustryDal, self).delete_datas(
            ids, v_soft, **kwargs
        )

    async def get_by_board_name(self, board_name: str) -> Any:
        """
        根据板块名称获取最新记录
        :param board_name: 板块名称
        :return: 板块记录
        """
        sql = (
            select(self.model)
            .where(self.model.board_name == board_name)
            .order_by(self.model.date_at.desc())
        )
        result = await self.db.execute(sql)
        return result.scalar_one_or_none()

    async def get_top_inflow(self, limit: int = 10) -> list:
        """
        获取净流入排名前N的板块
        :param limit: 返回数量
        :return: 板块列表
        """
        # 获取最新日期
        latest_date_subquery = select(func.max(self.model.date_at)).scalar_subquery()
        sql = (
            select(self.model)
            .where(self.model.date_at == latest_date_subquery)
            .order_by(self.model.net_inflow.desc())
            .limit(limit)
        )
        queryset = await self.db.scalars(sql)
        return [
            schemas.StockBoardIndustryOut.model_validate(i).model_dump()
            for i in queryset.all()
        ]

    async def get_top_change(self, limit: int = 10) -> list:
        """
        获取涨跌幅排名前N的板块
        :param limit: 返回数量
        :return: 板块列表
        """
        sql = (
            select(self.model)
            .where(self.model.date_at == self.model.date_at)
            .order_by(self.model.change_percent.desc())
            .limit(limit)
        )
        queryset = await self.db.scalars(sql)
        return [
            schemas.StockBoardIndustryOut.model_validate(i).model_dump()
            for i in queryset.all()
        ]

    async def export_query_list(
        self, header: list, params: params.StockBoardIndustryParams
    ) -> dict:
        """
        导出股票行业板块查询列表为 excel
        :param header: 表头字段
        :param params: 查询参数
        :return: 导出文件信息
        """
        params.limit = 1000000
        datas = await self.get_datas(**params.dict(), v_return_objs=True)

        # 获取表头
        row = list(map(lambda i: i.get("label"), header))
        rows = []

        for board in datas:
            data = []
            for item in header:
                field = item.get("field")
                # 通过反射获取对应的属性值
                value = getattr(board, field, "")

                data.append(value)
            rows.append(data)

        em = ExcelManage()
        em.create_excel("股票行业板块")
        em.write_list(rows, row)
        file_url = em.save_excel()
        em.close()
        return {"url": file_url, "filename": "股票行业板块.xlsx"}
