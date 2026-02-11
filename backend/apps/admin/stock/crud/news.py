#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/28
# @File           : news.py
# @IDE            : PyCharm
# @desc           : 新闻信息数据库 增删改查操作

from typing import Any
from sqlalchemy.orm.strategy_options import _AbstractLoad
from core.crud import DalBase
from utils.excel.excel_manage import ExcelManage
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, delete, update
from datetime import datetime
from apps.admin.stock import models, schemas, params


class NewsDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(NewsDal, self).__init__()
        self.db = db
        self.model = models.News
        self.schema = schemas.NewsOut

    async def get_select_datas(self) -> list:
        """
        获取选择数据，全部数据
        :return:
        """
        sql = select(self.model)
        queryset = await self.db.scalars(sql)
        return [schemas.NewsOut.model_validate(i).model_dump() for i in queryset.all()]

    async def create_data(
            self,
            data: schemas.NewsCreate,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        """
        创建新闻信息
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
            data: schemas.NewsUpdate,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        """
        更新单个新闻信息
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
        删除多个新闻信息
        :param ids: 数据集
        :param v_soft: 是否执行软删除
        :param kwargs: 其他更新字段
        """
        return await super(NewsDal, self).delete_datas(ids, v_soft, **kwargs)

    async def update_is_send(self, news_ids: list[int], is_send: int) -> None:
        """
        更新新闻的发送状态
        :param news_ids: 新闻ID列表
        :param is_send: 发送状态
        """
        await self.db.execute(
            update(self.model)
            .where(self.model.id.in_(news_ids))
            .values(is_send=is_send)
        )

    async def get_by_is_send(self, is_send: int = 0) -> list:
        """
        根据发送状态获取新闻列表
        :param is_send: 发送状态 0未发送 1已发送
        :return: 新闻列表
        """
        sql = select(self.model).where(self.model.is_send == is_send).order_by(
            self.model.priority.desc(),
            self.model.date_at.desc()
        )
        queryset = await self.db.scalars(sql)
        return [schemas.NewsOut.model_validate(i).model_dump() for i in queryset.all()]

    async def get_by_category(self, category: str) -> list:
        """
        根据分类获取新闻列表
        :param category: 分类
        :return: 新闻列表
        """
        sql = select(self.model).where(self.model.category == category).order_by(
            self.model.date_at.desc()
        )
        queryset = await self.db.scalars(sql)
        return [schemas.NewsOut.model_validate(i).model_dump() for i in queryset.all()]

    async def update_analyze_status(self, news_id: int, analyze_data: dict) -> None:
        """
        更新新闻分析状态和分析结果
        :param news_id: 新闻ID
        :param analyze_data: 分析数据
        """
        await self.db.execute(
            update(self.model)
            .where(self.model.id == news_id)
            .values(
                is_analyze=1,
                analyzed_at=datetime.now(),
                **analyze_data
            )
        )

    async def export_query_list(self, header: list, params: params.NewsParams) -> dict:
        """
        导出新闻查询列表为 excel
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
        priority_map = {1: '最高', 2: '高', 3: '中', 4: '低'}
        # 发送状态映射
        is_send_map = {0: '未发送', 1: '已发送'}
        # 分析状态映射
        is_analyze_map = {0: '未分析', 1: '已分析'}

        for news in datas:
            data = []
            for item in header:
                field = item.get("field")
                # 通过反射获取对应的属性值
                value = getattr(news, field, "")

                # 特殊字段处理
                if field == "priority":
                    value = priority_map.get(value, value)
                elif field == "is_send":
                    value = is_send_map.get(value, value)
                elif field == "is_analyze":
                    value = is_analyze_map.get(value, value)
                elif field == "has_concept_stocks":
                    value = "是" if value == 1 else "否"

                data.append(value)
            rows.append(data)

        em = ExcelManage()
        em.create_excel("新闻列表")
        em.write_list(rows, row)
        file_url = em.save_excel()
        em.close()
        return {"url": file_url, "filename": "新闻列表.xlsx"}
