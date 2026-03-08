#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version : 1.0
# @Create Time : 2025/02/15
# @File : stock_monitor_strategy.py
# @IDE : PyCharm
# @desc : 股票监听策略数据库 增删改查操作

from typing import Any, Optional
from sqlalchemy.orm.strategy_options import _AbstractLoad
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, update, func
from datetime import datetime
from apps.admin.stock import models, schemas
from utils.excel.excel_manage import ExcelManage


class StockMonitorStrategyDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(StockMonitorStrategyDal, self).__init__()
        self.db = db
        self.model = models.StockMonitorStrategy
        self.schema = schemas.StockMonitorStrategyOut

    async def create_data(
        self,
        data: schemas.StockMonitorStrategyCreate,
        v_options: list[_AbstractLoad] = None,
        v_return_obj: bool = False,
        v_schema: Any = None,
    ) -> Any:
        """创建股票监听策略"""
        obj = self.model(**data.model_dump())
        await self.flush(obj)
        return await self.out_dict(obj, v_options, v_return_obj, v_schema)

    async def put_data(
        self,
        data_id: int,
        data: schemas.StockMonitorStrategyUpdate,
        v_options: list[_AbstractLoad] = None,
        v_return_obj: bool = False,
        v_schema: Any = None,
    ) -> Any:
        """更新单个股票监听策略"""
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
        """删除多个股票监听策略"""
        return await super(StockMonitorStrategyDal, self).delete_datas(
            ids, v_soft, **kwargs
        )

    async def get_active_strategies(self, user_id: Optional[int] = None) -> list:
        """获取启用的监听策略"""
        sql = select(self.model).where(self.model.is_active == 1)
        if user_id:
            sql = sql.where(self.model.user_id == user_id)
        sql = sql.order_by(self.model.priority.asc(), self.model.created_at.desc())
        queryset = await self.db.scalars(sql)
        return [
            schemas.StockMonitorStrategyOut.model_validate(i).model_dump()
            for i in queryset.all()
        ]

    async def update_active_status(self, strategy_id: int, is_active: int) -> None:
        """更新策略的启用状态"""
        await self.db.execute(
            update(self.model)
            .where(self.model.id == strategy_id)
            .values(is_active=is_active)
        )

    async def update_trigger_info(
        self, strategy_id: int, trigger_time: datetime, trigger_count: int
    ) -> None:
        """更新策略触发信息"""
        await self.db.execute(
            update(self.model)
            .where(self.model.id == strategy_id)
            .values(
                last_trigger_time=trigger_time,
                last_trigger_count=trigger_count,
                trigger_count=self.model.trigger_count + trigger_count,
            )
        )

    async def get_by_user_id(self, user_id: int) -> list:
        """根据用户ID获取监听策略列表"""
        sql = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .order_by(self.model.created_at.desc())
        )
        queryset = await self.db.scalars(sql)
        return [
            schemas.StockMonitorStrategyOut.model_validate(i).model_dump()
            for i in queryset.all()
        ]

    async def get_by_stock_code(self, stock_code: str) -> list:
        """根据股票代码获取监听策略列表"""
        sql = (
            select(self.model)
            .where(self.model.stock_code == stock_code, self.model.is_active == 1)
            .order_by(self.model.priority.asc())
        )
        queryset = await self.db.scalars(sql)
        return [
            schemas.StockMonitorStrategyOut.model_validate(i).model_dump()
            for i in queryset.all()
        ]

    async def get_statistics(self, user_id: Optional[int] = None) -> dict:
        """获取策略统计信息"""
        sql = select(
            func.count(self.model.id).label("total"),
            func.sum(self.model.is_active == 1).label("active"),
            func.sum(self.model.trigger_count).label("total_triggers"),
        )
        if user_id:
            sql = sql.where(self.model.user_id == user_id)
        result = await self.db.execute(sql)
        row = result.one()
        return {
            "total": row.total or 0,
            "active": row.active or 0,
            "total_triggers": row.total_triggers or 0,
        }

    async def export_query_list(self, header: list, params) -> dict:
        """导出股票监听策略查询列表为 excel"""
        datas = await self.get_datas(**params.dict(), v_return_objs=True)

        row = list(map(lambda i: i.get("label"), header))
        rows = []

        is_active_map = {0: "禁用", 1: "启用"}
        strategy_type_map = {
            "limit_up": "涨停",
            "limit_down": "跌停",
            "open_board": "开板",
            "turnover": "换手",
            "breakout": "突破",
            "rebound": "反弹",
        }
        cooldown_type_map = {"same_day": "同一天内一次", "interval": "按间隔时间"}
        notify_method_map = {
            "system": "系统消息",
            "email": "邮件",
            "sms": "短信",
            "wechat": "微信",
        }
        notify_type_map = {
            "once": "仅一次",
            "always": "每次推送",
            "interval": "按间隔推送",
        }

        for data in datas:
            item = []
            for h in header:
                field = h.get("field")
                value = getattr(data, field, "")
                if field == "is_active" and value is not None:
                    value = is_active_map.get(value, value)
                elif field == "strategy_type" and value:
                    value = strategy_type_map.get(value, value)
                elif field == "cooldown_type" and value:
                    value = cooldown_type_map.get(value, value)
                elif field == "notify_method" and value:
                    value = notify_method_map.get(value, value)
                elif field == "notify_type" and value:
                    value = notify_type_map.get(value, value)
                item.append(value)
            rows.append(item)

        em = ExcelManage()
        em.create_excel("股票监听策略")
        em.write_list(rows, row)
        file_url = em.save_excel()
        em.close()
        return {"url": file_url, "filename": "股票监听策略.xlsx"}
