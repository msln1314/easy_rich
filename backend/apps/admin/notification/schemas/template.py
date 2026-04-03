# -*- coding: utf-8 -*-
"""通知模板 Schemas"""
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr


class NotificationTemplateCreate(BaseModel):
    """创建通知模板"""
    name: str = Field(..., description="模板名称")
    code: str = Field(..., description="模板编码")
    title_template: str = Field(..., description="标题模板")
    content_template: str = Field(..., description="内容模板")
    channel_types: Optional[List[str]] = Field(default=None, description="支持的渠道类型")
    description: Optional[str] = Field(default=None, description="模板描述")


class NotificationTemplateUpdate(BaseModel):
    """更新通知模板"""
    name: Optional[str] = None
    title_template: Optional[str] = None
    content_template: Optional[str] = None
    channel_types: Optional[List[str]] = None
    description: Optional[str] = None


class NotificationTemplateOut(BaseModel):
    """通知模板输出"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: str
    title_template: str
    content_template: str
    channel_types: Optional[List[str]] = None
    is_system: bool
    description: Optional[str] = None
    created_at: DatetimeStr
    updated_at: DatetimeStr