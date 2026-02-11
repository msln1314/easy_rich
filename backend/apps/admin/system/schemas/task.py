# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from typing import Optional, List
import re
from core.data_types import DatetimeStr


class TaskCreate(BaseModel):
    """
    定时任务调度表对应pydantic模型，与TaskModel字段一致
    """
    name: Optional[str] = Field(default=None, max_length=64, description='任务名称')
    jobstore: Optional[str] = Field(default='default', max_length=64, description='存储器')
    executor: Optional[str] = Field(default='default', max_length=64, description='执行器:将运行此作业的执行程序的名称')
    trigger: Optional[str] = Field(default=None, description='触发器:控制此作业计划的 trigger 对象(cron/interval/date)')
    trigger_args: Optional[str] = Field(default=None, description='触发器参数')
    job_class: Optional[str] = Field(default=None, description='任务函数')
    args: Optional[str] = Field(default=None, description='位置参数')
    kwargs: Optional[str] = Field(default=None, description='关键字参数')
    coalesce: Optional[bool] = Field(default=False, description='是否合并运行:是否在多个运行时间到期时仅运行作业一次')
    max_instances: Optional[int] = Field(default=1, description='最大实例数:允许的最大并发执行实例数')
    start_date: Optional[str] = Field(default=None, max_length=64, description='开始时间')
    end_date: Optional[str] = Field(default=None, max_length=64, description='结束时间')
    status: Optional[bool] = Field(default=True, description="是否启用(True:启用 False:禁用)")
    task_group_id: Optional[int] = Field(default=None, description='任务分组ID')


    @model_validator(mode='before')
    @classmethod
    def _normalize(cls, data):
        """前置归一化：字符串去空格、布尔/数字兼容转换。"""
        if isinstance(data, dict):
            for key in ('name', 'job_class', 'trigger', 'args', 'kwargs', 'jobstore', 'executor', 'trigger_args', 'start_date', 'end_date'):
                val = data.get(key)
                if isinstance(val, str):
                    data[key] = val.strip()
            for bkey in ('coalesce', 'status'):
                val = data.get(bkey)
                if isinstance(val, str):
                    lowered = val.strip().lower()
                    if lowered in {'true', '1', 'y', 'yes'}:
                        data[bkey] = True
                    elif lowered in {'false', '0', 'n', 'no'}:
                        data[bkey] = False
                elif isinstance(val, int):
                    data[bkey] = bool(val)
            val = data.get('max_instances')
            if isinstance(val, str) and val.strip().isdigit():
                data['max_instances'] = int(val.strip())
        return data

    @field_validator('trigger')
    @classmethod
    def _validate_trigger(cls, v: str | None) -> str | None:
        if v is None:
            return v
        allowed = {'cron', 'interval', 'date'}
        v = v.strip()
        if v not in allowed:
            raise ValueError('触发器必须为 cron/interval/date')
        return v

    @model_validator(mode='after')
    def _validate_dates(self):
        """跨字段校验：结束时间不得早于开始时间。"""
        if self.start_date and self.end_date:
            try:
                start = self.start_date
                end = self.end_date
            except Exception:
                raise ValueError('时间格式必须为 YYYY-MM-DD HH:MM:SS')
            if end < start:
                raise ValueError('结束时间不能早于开始时间')
        return self


class TaskUpdate(TaskCreate):
    """定时任务更新模型"""
    ...
    

class TaskOut(TaskCreate):
    """定时任务响应模型"""
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: DatetimeStr
    updated_at: DatetimeStr
    task_group: Optional['TaskGroupOut'] = Field(default=None, description='任务分组信息')
    # 添加临时字段
    is_active: Optional[bool] = Field(default=None, description='任务是否在调度器中运行')
    last_run_datetime: Optional[DatetimeStr] = Field(default=None, description='最近一次执行时间')




class TaskLogCreate(BaseModel):
    """
    定时任务调度日志表对应pydantic模型
    """

    model_config = ConfigDict(from_attributes=True)

    job_name: Optional[str] = Field(default=None, description='任务名称')
    job_group: Optional[str] = Field(default=None, description='任务组名')
    job_executor: Optional[str] = Field(default=None, description='任务执行器')
    invoke_target: Optional[str] = Field(default=None, description='调用目标字符串')
    job_args: Optional[str] = Field(default=None, description='位置参数')
    job_kwargs: Optional[str] = Field(default=None, description='关键字参数')
    job_trigger: Optional[str] = Field(default=None, description='任务触发器')
    job_message: Optional[str] = Field(default=None, description='日志信息')
    exception_info: Optional[str] = Field(default=None, description='异常信息')
    status: Optional[bool] = Field(default=False, description='任务状态:正常,失败')
    create_time: Optional[DatetimeStr] = Field(default=None, description='创建时间')


class TaskLogUpdate(TaskLogCreate):
    """定时任务调度日志表更新模型"""
    ...
    id: Optional[int] = Field(default=None, description='任务日志ID')


class TaskLogOut(TaskLogUpdate):
    """定时任务调度日志表响应模型"""
    model_config = ConfigDict(from_attributes=True)
    ...


class TaskGroupCreate(BaseModel):
    """
    定时任务分组表对应pydantic模型
    """
    name: str = Field(..., max_length=64, description='分组名称')
    description: Optional[str] = Field(default=None, description='分组描述')
    status: Optional[bool] = Field(default=True, description='分组状态:启动,停止')

    @model_validator(mode='before')
    @classmethod
    def _normalize(cls, data):
        """前置归一化：字符串去空格、布尔/数字兼容转换。"""
        if isinstance(data, dict):
            for key in ('name', 'description'):
                val = data.get(key)
                if isinstance(val, str):
                    data[key] = val.strip()
            val = data.get('status')
            if isinstance(val, str):
                lowered = val.strip().lower()
                if lowered in {'true', '1', 'y', 'yes'}:
                    data['status'] = True
                elif lowered in {'false', '0', 'n', 'no'}:
                    data['status'] = False
            elif isinstance(val, int):
                data['status'] = bool(val)
        return data


class TaskGroupUpdate(TaskGroupCreate):
    """定时任务分组更新模型"""
    ...


class TaskGroupOut(TaskGroupCreate):
    """定时任务分组响应模型"""
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: DatetimeStr
    updated_at: DatetimeStr
  
