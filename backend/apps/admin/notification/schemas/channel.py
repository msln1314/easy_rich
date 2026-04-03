# -*- coding: utf-8 -*-
"""通知渠道 Schemas"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr


class NotificationChannelCreate(BaseModel):
    """创建通知渠道"""
    channel_type: str = Field(..., description="渠道类型: email/wechat/system")
    channel_name: str = Field(..., description="渠道名称")
    channel_config: dict = Field(..., description="渠道配置")


class NotificationChannelUpdate(BaseModel):
    """更新通知渠道"""
    channel_name: Optional[str] = None
    channel_config: Optional[dict] = None
    is_enabled: Optional[bool] = None


class NotificationChannelOut(BaseModel):
    """通知渠道输出"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    channel_type: str
    channel_name: str
    channel_config: Optional[dict] = None
    is_enabled: bool
    verified: bool
    verified_at: Optional[DatetimeStr] = None
    created_at: DatetimeStr
    updated_at: DatetimeStr


class ChannelVerifyRequest(BaseModel):
    """验证渠道请求"""
    code: str = Field(..., description="验证码")


class ChannelTestRequest(BaseModel):
    """测试发送请求"""
    title: str = Field(default="测试通知", description="测试标题")
    content: str = Field(default="这是一条测试通知消息", description="测试内容")