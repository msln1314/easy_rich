#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version : 1.0
# @Create Time : 2025/02/15
# @File : stock_monitor_log.py
# @IDE : PyCharm
# @desc : 股票监听推送日志数据库 增删改查操作

from typing import Any, Optional
from sqlalchemy.orm.strategy_options import _AbstractLoad
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, update, func, delete
from datetime import datetime
from apps.admin.stock import models, schemas
from utils.excel.excel_manage import ExcelManage


class StockMonitorLogDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(StockMonitorLogDal, self).__init__()
        self.db = db
        self.model = models.StockMonitorLog
        self.schema = schemas.StockMonitorLogOut

    async def create_data(
        self,
        data: schemas.StockMonitorLogCreate,
        v_options: list[_AbstractLoad] = None,
        v_return_obj: bool = False,
        v_schema: Any = None,
    ) -> Any:
        """创建股票监听日志"""
        obj = self.model(**data.model_dump())
        await self.flush(obj)
        return await self.out_dict(obj, v_options, v_return_obj, v_schema)

    async def get_logs_by_strategy_id(self, strategy_id: int, limit: int = 100) -> list:
        """根据策略ID获取日志列表"""
        sql = (
            select(self.model)
            .where(self.model.strategy_id == strategy_id)
            .order_by(self.model.trigger_time.desc())
            .limit(limit)
        )
        queryset = await self.db.scalars(sql)
        return [
            schemas.StockMonitorLogOut.model_validate(i).model_dump()
            for i in queryset.all()
        ]

    async def get_logs_by_stock_code(self, stock_code: str, limit: int = 100) -> list:
        """根据股票代码获取日志列表"""
        sql = (
            select(self.model)
            .where(self.model.stock_code == stock_code)
            .order_by(self.model.trigger_time.desc())
            .limit(limit)
        )
        queryset = await self.db.scalars(sql)
        return [
            schemas.StockMonitorLogOut.model_validate(i).model_dump()
            for i in queryset.all()
        ]

    async def get_user_logs(self, user_id: int, limit: int = 100) -> list:
        """获取用户的日志列表"""
        sql = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .order_by(self.model.trigger_time.desc())
            .limit(limit)
        )
        queryset = await self.db.scalars(sql)
        return [
            schemas.StockMonitorLogOut.model_validate(i).model_dump()
            for i in queryset.all()
        ]

    async def update_notify_status(
        self,
        log_id: int,
        notify_status: int,
        notify_result: Optional[str] = None,
        error_message: Optional[str] = None,
    ) -> None:
        """更新推送状态"""
        update_data = {"notify_status": notify_status, "notify_time": datetime.now()}
        if notify_result:
            update_data["notify_result"] = notify_result
        if error_message:
            update_data["error_message"] = error_message

        await self.db.execute(
            update(self.model).where(self.model.id == log_id).values(**update_data)
        )

    async def get_statistics(
        self, user_id: Optional[int] = None, days: int = 7
    ) -> dict:
        """获取日志统计信息"""
        start_time = datetime.now() - timedelta(days=days)

        sql = select(
            func.count(self.model.id).label("total"),
            func.sum(self.model.notify_status == 1).label("success"),
            func.sum(self.model.notify_status == 2).label("failed"),
            func.count(func.distinct(self.model.stock_code)).label("stock_count"),
        ).where(self.model.trigger_time >= start_time)

        if user_id:
            sql = sql.where(self.model.user_id == user_id)

        result = await self.db.execute(sql)
        row = result.one()

        return {
            "total_triggers": row.total or 0,
            "success_notifications": row.success or 0,
            "failed_notifications": row.failed or 0,
            "monitored_stocks": row.stock_count or 0,
            "period_days": days,
        }

    async def get_recent_logs(
        self, user_id: Optional[int] = None, hours: int = 24
    ) -> list:
        """获取最近日志"""
        start_time = datetime.now() - timedelta(hours=hours)

        sql = select(self.model).where(self.model.trigger_time >= start_time)

        if user_id:
            sql = sql.where(self.model.user_id == user_id)

        sql = sql.order_by(self.model.trigger_time.desc()).limit(50)
        queryset = await self.db.scalars(sql)
        return [
            schemas.StockMonitorLogOut.model_validate(i).model_dump()
            for i in queryset.all()
        ]

    async def delete_old_logs(self, days: int = 30) -> int:
        """删除旧日志"""
        cutoff_time = datetime.now() - timedelta(days=days)
        result = await self.db.execute(
            delete(self.model).where(self.model.trigger_time < cutoff_time)
        )
        await self.db.commit()
        return result.rowcount

    async def export_query_list(self, header: list, params) -> dict:
        """导出股票监听日志查询列表为 excel"""
        datas = await self.get_datas(**params.dict(), v_return_objs=True)

        row = list(map(lambda i: i.get("label"), header))
        rows = []

        strategy_type_map = {
            "limit_up": "涨停",
            "limit_down": "跌停",
            "open_board": "开板",
            "turnover": "换手",
            "breakout": "突破",
            "rebound": "反弹",
        }
        notify_status_map = {0: "待推送", 1: "推送成功", 2: "推送失败"}
        notify_method_map = {
            "system": "系统消息",
            "email": "邮件",
            "sms": "短信",
            "wechat": "微信",
        }

        for data in datas:
            item = []
            for h in header:
                field = h.get("field")
                value = getattr(data, field, "")
                if field == "strategy_type" and value:
                    value = strategy_type_map.get(value, value)
                elif field == "notify_status" and value is not None:
                    value = notify_status_map.get(value, value)
                elif field == "notify_method" and value:
                    value = notify_method_map.get(value, value)
                item.append(value)
            rows.append(item)

        em = ExcelManage()
        em.create_excel("股票监听日志")
        em.write_list(rows, row)
        file_url = em.save_excel()
        em.close()
        return {"url": file_url, "filename": "股票监听日志.xlsx"}
