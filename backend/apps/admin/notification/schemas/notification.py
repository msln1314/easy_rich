# -*- coding: utf-8 -*-
"""通知相关 Schemas"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr


class NotificationLogOut(BaseModel):
    """通知日志输出"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    channel_type: str
    template_code: Optional[str] = None
    title: str
    content: str
    status: str
    error_msg: Optional[str] = None
    sent_at: Optional[DatetimeStr] = None
    extra_data: Optional[dict] = None
    created_at: DatetimeStr


class SystemNotificationOut(BaseModel):
    """系统通知输出"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str
    content: str
    notification_type: str
    is_read: bool
    read_at: Optional[DatetimeStr] = None
    link: Optional[str] = None
    extra_data: Optional[dict] = None
    created_at: DatetimeStr


class SystemNotificationListOut(BaseModel):
    """系统通知列表输出"""
    total: int
    items: List[SystemNotificationOut]
    unread_count: int


class NotificationSendRequest(BaseModel):
    """发送通知请求"""
    user_id: int = Field(..., description="用户ID")
    title: str = Field(..., description="通知标题")
    content: str = Field(..., description="通知内容")
    channels: Optional[List[str]] = Field(default=None, description="通知渠道列表")
    template_code: Optional[str] = Field(default=None, description="模板编码")
    extra_data: Optional[dict] = Field(default=None, description="额外数据")


class NotificationTestRequest(BaseModel):
    """测试通知请求"""
    channel_id: int = Field(..., description="渠道ID")
    title: str = Field(default="测试通知", description="测试标题")
    content: str = Field(default="这是一条测试通知消息", description="测试内容")


class UnreadCountOut(BaseModel):
    """未读数量输出"""
    unread_count: int