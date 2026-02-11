# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from core.data_types import DatetimeStr


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
    job_id: Optional[int] = Field(default=None, description='任务ID')


class TaskLogUpdate(TaskLogCreate):
    """定时任务调度日志表更新模型"""
    ...
    id: Optional[int] = Field(default=None, description='任务日志ID')


class TaskLogOut(TaskLogUpdate):
    """定时任务调度日志表响应模型"""
    model_config = ConfigDict(from_attributes=True)
    id: int
