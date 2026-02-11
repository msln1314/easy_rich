#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/02/03
# @File           : task.py
# @IDE            : PyCharm
# @desc           : 定时任务日志 CRUD 操作

from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from core.crud import DalBase
from core.exception import CustomException
from apps.admin.system import models, schemas


class TaskLogDal(DalBase):
    """任务日志数据访问层 - sys_task_log"""

    def __init__(self, db: AsyncSession):
        super().__init__(db, models.TaskLogModel, schemas.TaskLogOut)

    async def get_task_logs(
        self,
        page: int = 1,
        limit: int = 10,
        v_schema: Any = None,
        v_order: str | None = None,
        v_order_field: str | None = None,
        job_id: int | None = None
    ):
        """获取任务日志列表"""
        query = select(self.model)

        # 按任务ID过滤
        if job_id:
            query = query.where(self.model.job_id == job_id)

        # 排序
        if v_order_field and hasattr(self.model, v_order_field):
            order_field = getattr(self.model, v_order_field)
            if v_order and v_order.lower() == 'desc':
                query = query.order_by(order_field.desc())
            else:
                query = query.order_by(order_field.asc())
        else:
            query = query.order_by(self.model.created_at.desc())

        # 分页
        total = await self.get_count(v_sql=query)
        query = query.offset((page - 1) * limit).limit(limit)

        # 执行查询
        result = await self.db.execute(query)
        logs = result.scalars().all()

        if v_schema:
            return [v_schema.model_validate(log).model_dump() for log in logs], total

        return logs, total

    async def get_task_log(self, _id: int, v_schema: Any = None, v_return_none: bool = False):
        """获取单个任务日志"""
        query = select(self.model).where(self.model.id == _id)
        result = await self.db.execute(query)
        log = result.scalars().first()

        if not log and not v_return_none:
            raise CustomException(status_code=404, msg="日志不存在")

        if not log:
            return None

        if v_schema:
            return v_schema.model_validate(log).model_dump()

        return log

    async def create_task_log(self, data: schemas.TaskLogCreate):
        """创建任务日志"""
        data_dict = data.model_dump()
        obj = self.model(**data_dict)
        self.db.add(obj)
        await self.db.flush()
        await self.db.commit()
        return {'id': obj.id}

    async def delete_task_log(self, _id: int) -> bool:
        """删除任务日志"""
        result = await self.db.execute(
            delete(self.model).where(self.model.id == _id)
        )
        await self.db.commit()
        return result.rowcount > 0

    async def clear_task_logs(self, job_id: int | None = None) -> int:
        """清空任务日志"""
        query = delete(self.model)
        if job_id:
            query = query.where(self.model.job_id == job_id)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount

    async def get_last_run(self, task_id: int):
        """获取任务最近一次执行记录"""
        query = (
            select(self.model)
            .where(self.model.job_id == task_id)
            .order_by(self.model.created_at.desc())
            .limit(1)
        )
        result = await self.db.execute(query)
        return result.scalars().first()
