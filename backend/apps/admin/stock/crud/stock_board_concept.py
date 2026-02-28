#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/01/31
# @File           : stock_board_concept.py
# @IDE            : PyCharm
# @desc           : 股票概念板块数据库 增删改查操作

from typing import Any, List, Dict
from sqlalchemy.orm.strategy_options import _AbstractLoad
from core.crud import DalBase
from utils.excel.excel_manage import ExcelManage
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, delete, update, or_, and_, func
from datetime import datetime, date
from apps.admin.stock import models, schemas, params
from core.logger import logger


class StockBoardConceptDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(StockBoardConceptDal, self).__init__()
        self.db = db
        self.model = models.StockBoardConcept
        self.schema = schemas.StockBoardConceptOut

    async def get_concept_data_from_ths(self) -> List[Dict[str, Any]]:
        """
        从同花顺获取概念板块数据

        模拟从同花顺获取概念板块数据
        """
        try:
            # 模拟从同花顺获取概念板块数据
            concept_data = [
                {
                    "board_name": "人工智能",
                    "board_code": "GN0001",
                    "total_amount": 125.6,
                    "change_percent": 2.5,
                    "stock_count": 35,
                    "leading_stock": "科大讯飞",
                    "leading_stock_code": "002230",
                    "leading_stock_change": 3.2,
                    "up_count": 25,
                    "down_count": 8,
                    "net_inflow": 15.3,
                    "average_price": 45.6,
                    "turnover_rate": 1.2,
                    "market_cap": 8500,
                    "total_volume": 1250,
                    "create_time": datetime.now(),
                    "update_time": datetime.now(),
                },
                {
                    "board_name": "新能源汽车",
                    "board_code": "GN0002",
                    "total_amount": 85.3,
                    "change_percent": -1.8,
                    "stock_count": 28,
                    "leading_stock": "比亚迪",
                    "leading_stock_code": "002594",
                    "leading_stock_change": -2.1,
                    "up_count": 12,
                    "down_count": 16,
                    "net_inflow": -8.7,
                    "average_price": 78.5,
                    "turnover_rate": 0.9,
                    "market_cap": 12000,
                    "total_volume": 850,
                    "create_time": datetime.now(),
                    "update_time": datetime.now(),
                },
                {
                    "board_name": "半导体",
                    "board_code": "GN0003",
                    "total_amount": 65.8,
                    "change_percent": 3.1,
                    "stock_count": 22,
                    "leading_stock": "中芯国际",
                    "leading_stock_code": "688981",
                    "leading_stock_change": 4.5,
                    "up_count": 18,
                    "down_count": 4,
                    "net_inflow": 12.6,
                    "average_price": 65.2,
                    "turnover_rate": 1.5,
                    "market_cap": 6800,
                    "total_volume": 658,
                    "create_time": datetime.now(),
                    "update_time": datetime.now(),
                },
                {
                    "board_name": "医药生物",
                    "board_code": "GN0004",
                    "total_amount": 45.2,
                    "change_percent": 0.8,
                    "stock_count": 40,
                    "leading_stock": "恒瑞医药",
                    "leading_stock_code": "600276",
                    "leading_stock_change": 1.2,
                    "up_count": 22,
                    "down_count": 13,
                    "net_inflow": 3.4,
                    "average_price": 52.1,
                    "turnover_rate": 0.6,
                    "market_cap": 9200,
                    "total_volume": 452,
                    "create_time": datetime.now(),
                    "update_time": datetime.now(),
                },
                {
                    "board_name": "新材料",
                    "board_code": "GN0005",
                    "total_amount": 38.7,
                    "change_percent": 1.5,
                    "stock_count": 18,
                    "leading_stock": "三一重工",
                    "leading_stock_code": "600031",
                    "leading_stock_change": 2.3,
                    "up_count": 15,
                    "down_count": 3,
                    "net_inflow": 6.8,
                    "average_price": 48.9,
                    "turnover_rate": 0.8,
                    "market_cap": 5600,
                    "total_volume": 387,
                    "create_time": datetime.now(),
                    "update_time": datetime.now(),
                },
                {
                    "board_name": "5G通信",
                    "board_code": "GN0006",
                    "total_amount": 52.4,
                    "change_percent": -0.5,
                    "stock_count": 25,
                    "leading_stock": "中兴通讯",
                    "leading_stock_code": "000063",
                    "leading_stock_change": -1.1,
                    "up_count": 10,
                    "down_count": 15,
                    "net_inflow": -2.3,
                    "average_price": 38.7,
                    "turnover_rate": 0.7,
                    "market_cap": 7400,
                    "total_volume": 524,
                    "create_time": datetime.now(),
                    "update_time": datetime.now(),
                },
                {
                    "board_name": "云计算",
                    "board_code": "GN0007",
                    "total_amount": 28.9,
                    "change_percent": 2.8,
                    "stock_count": 15,
                    "leading_stock": "浪潮信息",
                    "leading_stock_code": "000977",
                    "leading_stock_change": 3.6,
                    "up_count": 12,
                    "down_count": 3,
                    "net_inflow": 8.2,
                    "average_price": 29.4,
                    "turnover_rate": 1.1,
                    "market_cap": 4200,
                    "total_volume": 289,
                    "create_time": datetime.now(),
                    "update_time": datetime.now(),
                },
                {
                    "board_name": "大数据",
                    "board_code": "GN0008",
                    "total_amount": 22.5,
                    "change_percent": 1.9,
                    "stock_count": 12,
                    "leading_stock": "东方财富",
                    "leading_stock_code": "300059",
                    "leading_stock_change": 2.4,
                    "up_count": 8,
                    "down_count": 4,
                    "net_inflow": 5.1,
                    "average_price": 18.7,
                    "turnover_rate": 0.9,
                    "market_cap": 3800,
                    "total_volume": 225,
                    "create_time": datetime.now(),
                    "update_time": datetime.now(),
                },
                {
                    "board_name": "物联网",
                    "board_code": "GN0009",
                    "total_amount": 19.8,
                    "change_percent": 0.3,
                    "stock_count": 10,
                    "leading_stock": "移远通信",
                    "leading_stock_code": "002913",
                    "leading_stock_change": 0.8,
                    "up_count": 6,
                    "down_count": 4,
                    "net_inflow": 1.2,
                    "average_price": 19.5,
                    "turnover_rate": 0.5,
                    "market_cap": 3200,
                    "total_volume": 198,
                    "create_time": datetime.now(),
                    "update_time": datetime.now(),
                },
                {
                    "board_name": "区块链",
                    "board_code": "GN0010",
                    "total_amount": 15.6,
                    "change_percent": -1.2,
                    "stock_count": 8,
                    "leading_stock": "广电运通",
                    "leading_stock_code": "002152",
                    "leading_stock_change": -2.1,
                    "up_count": 3,
                    "down_count": 5,
                    "net_inflow": -1.8,
                    "average_price": 15.9,
                    "turnover_rate": 0.4,
                    "market_cap": 2800,
                    "total_volume": 156,
                    "create_time": datetime.now(),
                    "update_time": datetime.now(),
                },
            ]

            return concept_data
        except Exception as e:
            logger.error(f"获取概念板块数据失败: {str(e)}")
            return []

    async def sync_concept_data(self, concept_data: List[Dict[str, Any]]) -> int:
        """
        同步概念板块数据

        将概念板块数据保存到数据库
        """
        try:
            # 先清空现有数据
            await self.delete_datas([])

            # 插入新数据
            created_count = 0
            for data in concept_data:
                # 转换数据格式
                create_data = schemas.StockBoardConceptCreate(**data)
                await self.create_data(create_data)
                created_count += 1

            return created_count
        except Exception as e:
            logger.error(f"同步概念板块数据失败: {str(e)}")
            return 0

    async def create_data(
        self,
        data: schemas.StockBoardConceptCreate,
        v_options: list[_AbstractLoad] = None,
        v_return_obj: bool = False,
        v_schema: Any = None,
    ) -> Any:
        """
        创建股票概念板块
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
        data: schemas.StockBoardConceptUpdate,
        v_options: list[_AbstractLoad] = None,
        v_return_obj: bool = False,
        v_schema: Any = None,
    ) -> Any:
        """
        更新单个股票概念板块
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
        删除多个股票概念板块
        :param ids: 数据集
        :param v_soft: 是否执行软删除
        :param kwargs: 其他更新字段
        """
        return await super(StockBoardConceptDal, self).delete_datas(
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

    async def get_top_inflow(self, limit: int = 10, date_at: date = None) -> list:
        """
        获取净流入排名前N的概念板块
        :param limit: 返回数量
        :param date_at: 指定日期，默认最新
        :return: 概念列表
        """
        sql = select(self.model)

        if date_at:
            sql = sql.where(self.model.date_at == date_at)
        else:
            # 获取最新日期
            latest_date_subquery = select(
                func.max(self.model.date_at)
            ).scalar_subquery()
            sql = sql.where(self.model.date_at == latest_date_subquery)

        sql = sql.order_by(self.model.net_inflow.desc()).limit(limit)
        queryset = await self.db.scalars(sql)
        return [
            schemas.StockBoardConceptOut.model_validate(i).model_dump()
            for i in queryset.all()
        ]

    async def get_top_change(self, limit: int = 10, date_at: date = None) -> list:
        """
        获取涨跌幅排名前N的概念板块
        :param limit: 返回数量
        :param date_at: 指定日期，默认最新
        :return: 概念列表
        """
        sql = select(self.model)

        if date_at:
            sql = sql.where(self.model.date_at == date_at)
        else:
            # 获取最新日期
            latest_date_subquery = select(
                func.max(self.model.date_at)
            ).scalar_subquery()
            sql = sql.where(self.model.date_at == latest_date_subquery)

        sql = sql.order_by(self.model.change_percent.desc()).limit(limit)
        queryset = await self.db.scalars(sql)
        return [
            schemas.StockBoardConceptOut.model_validate(i).model_dump()
            for i in queryset.all()
        ]

    async def get_daily_change_ranking(
        self, date_at: date = None, limit: int = 50
    ) -> list:
        """
        获取当日概念板块涨跌幅排行
        :param date_at: 指定日期，默认最新
        :param limit: 返回数量
        :return: 概念列表
        """
        sql = select(self.model)

        if date_at:
            sql = sql.where(self.model.date_at == date_at)
        else:
            # 获取最新日期
            latest_date_subquery = select(
                func.max(self.model.date_at)
            ).scalar_subquery()
            sql = sql.where(self.model.date_at == latest_date_subquery)

        sql = sql.order_by(self.model.change_percent.desc()).limit(limit)
        queryset = await self.db.scalars(sql)
        return [
            schemas.StockBoardConceptOut.model_validate(i).model_dump()
            for i in queryset.all()
        ]

    async def get_concept_trend_data(
        self, start_date: date, end_date: date, concept_names: list = None
    ) -> list:
        """
        获取概念板块趋势数据
        :param start_date: 开始日期
        :param end_date: 结束日期
        :param concept_names: 概念名称列表，为空则查询所有
        :return: 趋势数据
        """
        sql = select(self.model).where(
            and_(self.model.date_at >= start_date, self.model.date_at <= end_date)
        )

        if concept_names:
            sql = sql.where(self.model.board_name.in_(concept_names))

        sql = sql.order_by(self.model.date_at, self.model.change_percent.desc())
        result = await self.db.execute(sql)
        items = result.scalars().all()

        return [
            schemas.StockBoardConceptOut.model_validate(i).model_dump() for i in items
        ]

    async def get_heatmap_data(self, date_at: date = None, limit: int = 100) -> list:
        """
        获取热力图数据
        :param date_at: 指定日期，默认最新
        :param limit: 返回数量
        :return: 热力图数据
        """
        sql = select(self.model).where(self.model.change_percent.isnot(None))

        if date_at:
            sql = sql.where(self.model.date_at == date_at)
        else:
            # 获取最新日期
            latest_date_subquery = select(
                func.max(self.model.date_at)
            ).scalar_subquery()
            sql = sql.where(self.model.date_at == latest_date_subquery)

        sql = sql.order_by(self.model.change_percent.desc()).limit(limit)
        queryset = await self.db.scalars(sql)
        return [
            schemas.StockBoardConceptOut.model_validate(i).model_dump()
            for i in queryset.all()
        ]

    async def get_concept_list(self) -> list:
        """
        获取所有概念板块列表
        :return: 概念列表
        """
        subquery = select(self.model.board_name, self.model.board_code).distinct()
        result = await self.db.execute(subquery)
        items = result.all()

        return [
            {"concept_name": item.board_name, "concept_code": item.board_code}
            for item in items
        ]

    async def export_query_list(
        self, header: list, params: params.StockBoardConceptParams
    ) -> dict:
        """
        导出股票概念板块查询列表为 excel
        :param header: 表头字段
        :param params: 查询参数
        :return: 导出文件信息
        """
        params.limit = 1000000
        datas = await self.get_datas(**params.dict(), v_return_objs=True)

        # 获取表头
        row = list(map(lambda i: i.get("label"), header))
        rows = []

        for concept in datas:
            data = []
            for item in header:
                field = item.get("field")
                # 通过反射获取对应的属性值
                value = getattr(concept, field, "")

                data.append(value)
            rows.append(data)

        em = ExcelManage()
        em.create_excel("股票概念板块")
        em.write_list(rows, row)
        file_url = em.save_excel()
        em.close()
        return {"url": file_url, "filename": "股票概念板块.xlsx"}

    async def get_analysis_summary(self, date_at: date = None) -> dict:
        """
        获取概念板块分析概览
        :param date_at: 指定日期，默认最新
        :return: 分析概览
        """
        sql = select(self.model)

        if date_at:
            sql = sql.where(self.model.date_at == date_at)
        else:
            # 获取最新日期
            latest_date_subquery = select(
                func.max(self.model.date_at)
            ).scalar_subquery()
            sql = sql.where(self.model.date_at == latest_date_subquery)

        result = await self.db.execute(sql)
        items = result.scalars().all()

        if not items:
            return {
                "total_concepts": 0,
                "rising_concepts": 0,
                "falling_concepts": 0,
                "flat_concepts": 0,
                "total_inflow": 0,
                "total_amount": 0,
                "best_concept": None,
                "worst_concept": None,
            }

        # 计算统计数据
        total_concepts = len(items)
        rising_concepts = len(
            [item for item in items if item.change_percent and item.change_percent > 0]
        )
        falling_concepts = len(
            [item for item in items if item.change_percent and item.change_percent < 0]
        )
        flat_concepts = total_concepts - rising_concepts - falling_concepts

        total_inflow = sum(item.net_inflow or 0 for item in items)
        total_amount = sum(item.total_amount or 0 for item in items)

        # 找出最佳和最差概念
        sorted_by_change = sorted(
            items, key=lambda x: x.change_percent or 0, reverse=True
        )
        best_concept = (
            schemas.StockBoardConceptOut.model_validate(
                sorted_by_change[0]
            ).model_dump()
            if sorted_by_change
            else None
        )
        worst_concept = (
            schemas.StockBoardConceptOut.model_validate(
                sorted_by_change[-1]
            ).model_dump()
            if sorted_by_change
            else None
        )

        return {
            "total_concepts": total_concepts,
            "rising_concepts": rising_concepts,
            "falling_concepts": falling_concepts,
            "flat_concepts": flat_concepts,
            "total_inflow": total_inflow,
            "total_amount": total_amount,
            "best_concept": best_concept,
            "worst_concept": worst_concept,
            "date": date_at or items[0].date_at.strftime("%Y-%m-%d"),
        }
