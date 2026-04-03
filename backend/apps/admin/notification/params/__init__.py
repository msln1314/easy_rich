# -*- coding: utf-8 -*-
"""通知模块请求参数"""
from typing import Optional, List
from pydantic import BaseModel, Field


class NotificationRuleCreate(BaseModel):
    """创建通知规则"""
    rule_name: str = Field(..., description="规则名称")
    rule_type: str = Field(..., description="规则类型: holiday/earnings/dividend/unlock/custom")
    event_type_filter: Optional[str] = Field(None, description="事件类型过滤")
    stock_codes: Optional[List[str]] = Field(None, description="股票代码列表")
    condition_config: dict = Field(..., description="条件配置")
    action_config: dict = Field(..., description="动作配置")
    priority: int = Field(default=0, description="优先级")
    valid_from: Optional[str] = Field(None, description="有效期开始")
    valid_to: Optional[str] = Field(None, description="有效期结束")


class NotificationRuleUpdate(BaseModel):
    """更新通知规则"""
    rule_name: Optional[str] = None
    event_type_filter: Optional[str] = None
    stock_codes: Optional[List[str]] = None
    condition_config: Optional[dict] = None
    action_config: Optional[dict] = None
    priority: Optional[int] = None
    is_enabled: Optional[bool] = None
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None


class NotificationRuleOut(BaseModel):
    """通知规则输出"""
    from core.data_types import DatetimeStr

    model_config = {"from_attributes": True}

    id: int
    user_id: int
    rule_name: str
    rule_type: str
    event_type_filter: Optional[str] = None
    stock_codes: Optional[List[str]] = None
    condition_config: Optional[dict] = None
    action_config: Optional[dict] = None
    priority: int
    is_enabled: bool
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None
    last_triggered_at: Optional[str] = None
    created_at: DatetimeStr
    updated_at: DatetimeStr


class NotificationRuleListOut(BaseModel):
    """通知规则列表输出"""
    total: int
    items: List[NotificationRuleOut]