#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:18
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 数据库 增删改查操作

from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from core.crud import DalBase
from core.exception import CustomException
from apps.admin.system import models, schemas
from core.ap_scheduler import SchedulerUtil


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

        return [schemas.TaskLogOut.model_validate(log).model_dump() for log in logs], total

    async def get_task_log(self, _id: int, v_return_none: bool = False):
        """获取单个任务日志"""
        query = select(self.model).where(self.model.id == _id)
        result = await self.db.execute(query)
        log = result.scalars().first()

        if not log and not v_return_none:
            raise CustomException(status_code=404, msg="日志不存在")

        if not log:
            return None

        return schemas.TaskLogOut.model_validate(log).model_dump()

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


class TaskDal(DalBase):
    """
    任务管理数据访问层 - sys_task
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db, models.TaskModel, schemas.TaskOut)

    async def get_task(
        self,
        _id: int | None = None,
        v_return_none: bool = False,
        v_schema: Any = None
    ):
        """
        获取单个数据，默认使用 ID 查询

        包括临时字段 last_run_datetime，is_active
        is_active: 只有在调度器中存在相同 _id 才表示任务添加成功，任务状态才为 True
        last_run_datetime: 在 sys_task_log 中获取该任务最近一次执行完成的时间

        :param _id: 数据 ID
        :param v_return_none: 是否返回空 None，否则抛出异常，默认抛出异常
        :param v_schema: 指定使用的序列化对象
        """
        if not _id:
            raise CustomException(status_code=400, msg="ID不能为空")
        
        task = await self.get_data(_id, v_return_none=v_return_none)

       

        if not task and not v_return_none:
            raise CustomException(status_code=404, msg="任务不存在")

        if not task:
            return None

        # 检查任务是否在调度器中
        scheduler = SchedulerUtil()
        job = scheduler.get_job(str(_id))
        task.is_active = job is not None

        # 获取最近一次执行时间
        log_dal = TaskLogDal(self.db)
        last_run = await log_dal.get_last_run(_id)
        task.last_run_datetime = last_run.created_at if last_run else None

        # 修复非法的 trigger 值
        if task.trigger not in ('cron', 'interval', 'date'):
            task.trigger = 'cron'  # 设置默认值

        if v_schema:
            return v_schema.model_validate(task).model_dump()
        return task

    async def get_tasks(
        self,
        v_schema: Any = None,
        v_order: str | None = None,
        v_order_field: str | None = None,
        **kwargs
    ):
        """
        获取任务信息列表

        添加了两个临时字段
        is_active: 只有在调度器中存在相同 _id 才表示任务添加成功，任务状态才为 True
        last_run_datetime: 在 sys_task_log 中获取该任务最近一次执行完成的时间
        """
        # query = select(self.model)

        # # 排序
        # if v_order_field and hasattr(self.model, v_order_field):
        #     order_field = getattr(self.model, v_order_field)
        #     if v_order and v_order.lower() == 'desc':
        #         query = query.order_by(order_field.desc())
        #     else:
        #         query = query.order_by(order_field.asc())
        # else:
        #     query = query.order_by(self.model.created_at.desc())

        # # 分页
        # total = await self.get_count(v_sql=query)
        # query = query.offset((page - 1) * limit).limit(limit)

        # # 执行查询
        # result = await self.db.execute(query)
        # tasks = result.scalars().all()

        tasks, total = await self.get_datas(
            **kwargs,
            v_order='desc',
            v_order_field='created_at',
            v_schema=v_schema,
            v_return_count=True
    )

        # 获取任务状态和最后执行时间
        scheduler = SchedulerUtil()
        log_dal = TaskLogDal(self.db)

        for task in tasks:
            job = scheduler.get_job(str(task.id))
            task.is_active = job is not None

            last_run = await log_dal.get_last_run(task.id)
            task.last_run_datetime = last_run.created_at if last_run else None

            # 修复非法的 trigger 值
            if task.trigger not in ('cron', 'interval', 'date'):
                task.trigger = 'cron'  # 设置默认值

        if v_schema:
            return [v_schema.model_validate(task).model_dump() for task in tasks], total

        return [schemas.TaskOut.model_validate(task).model_dump() for task in tasks], total

    async def create_task(self, data: schemas.TaskCreate):
        """
        创建任务
        """
        data_dict = data.model_dump()

        # 获取任务启用状态
        is_active = data_dict.get('status', False)

        # 直接使用 TaskModel 的字段,不进行映射
        obj = self.model(**data_dict)
        self.db.add(obj)
        await self.db.flush()

        # 如果任务启用状态，则添加到调度器
        if is_active:
            SchedulerUtil().add_job(obj)

        await self.db.commit()

        return {
            "subscribe_number": 1 if is_active else 0,
            "is_active": is_active
        }

    async def put_task(self, _id: int, data: schemas.TaskUpdate):
        """
        更新任务
        """
        # 获取任务
        task = await self.get_data(_id, v_return_none=True)
        if not task:
            raise CustomException(status_code=404, msg="任务不存在")

        # 更新任务信息 - 直接使用 TaskModel 字段
        update_data = data.model_dump(exclude_unset=True, exclude={'status'})
        is_active = data.status if hasattr(data, 'status') else task.status

        for field, value in update_data.items():
            setattr(task, field, value)

        # 更新调度器中的任务
        scheduler = SchedulerUtil()
        scheduler.remove_job(str(_id))
        if is_active:
            scheduler.add_job(task)

        await self.db.flush()
      
        return {
            "subscribe_number": 1 if is_active else 0,
            "is_active": is_active
        }

    async def delete_task(self, _id: int) -> bool:
        """
        删除任务
        """
        # 从调度器中移除任务
        SchedulerUtil().remove_job(str(_id))

        # 删除任务
        await self.delete_datas(ids=[_id])

    async def run_once_task(self, _id: int) -> bool:
        """
        执行一次任务
        """
        task = await self.get_data(_id, v_return_none=True)
        if not task:
            raise CustomException(status_code=404, msg="任务不存在")

        # 调用 scheduler.run_job 创建一次性执行任务
        scheduler = SchedulerUtil()
        scheduler.run_job(task)

        return True


class TaskGroupDal(DalBase):
    """任务分组数据访问层 - sys_task_group"""

    def __init__(self, db: AsyncSession):
        super().__init__(db, models.TaskGroupModel, schemas.TaskGroupOut)

    async def get_task_groups(
        self,
        page: int = 1,
        limit: int = 10,
        v_schema: Any = None
    ):
        """获取任务分组列表"""
        query = select(self.model)

        # 排序
        query = query.order_by(self.model.created_at.desc())

        # 分页
        total = await self.get_count(v_sql=query)
        query = query.offset((page - 1) * limit).limit(limit)

        # 执行查询
        result = await self.db.execute(query)
        groups = result.scalars().all()

        if v_schema:
            return [v_schema.model_validate(group).model_dump() for group in groups], total
        return [schemas.TaskGroupOut.model_validate(group).model_dump() for group in groups], total

    async def create_task_group(self, data: schemas.TaskGroupCreate):
        """创建任务分组"""
        data_dict = data.model_dump()
        obj = self.model(**data_dict)
        self.db.add(obj)
        await self.db.flush()
        await self.db.commit()
        return {'id': obj.id}

    async def update_task_group(self, _id: int, data: schemas.TaskGroupUpdate):
        """更新任务分组"""
        task = await self.get_data(_id, v_return_none=True)
        if not task:
            raise CustomException(status_code=404, msg="任务分组不存在")

        data_dict = data.model_dump(exclude_unset=True)
        for field, value in data_dict.items():
            setattr(task, field, value)

        await self.db.commit()
        await self.db.refresh(task)
        return {'id': task.id}

    async def delete_task_group(self, _id: int) -> bool:
        """删除任务分组"""
        result = await self.db.execute(
            delete(self.model).where(self.model.id == _id)
        )
        await self.db.commit()
        return result.rowcount > 0
