# -*- coding: utf-8 -*-
"""通知渠道模型"""
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime, Integer, Text, Index
from db.db_base import BaseModel


class NotificationChannel(BaseModel):
    """通知渠道配置表"""
    __tablename__ = "notification_channel"
    __table_args__ = (
        Index("idx_user_channel", "user_id", "channel_type"),
        {"comment": "通知渠道配置表"},
    )

    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="用户ID")
    channel_type: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="渠道类型: email/wechat/system"
    )
    channel_name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="渠道名称"
    )
    channel_config: Mapped[dict | None] = mapped_column(
        Text, nullable=True, comment="渠道配置JSON"
    )
    # email: {"address": "user@example.com"}
    # wechat: {"push_type": "serverchan", "sendkey": "xxx"}
    is_enabled: Mapped[bool] = mapped_column(
        Boolean, default=True, comment="是否启用"
    )
    verified: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="是否已验证"
    )
    verify_code: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="验证码"
    )
    verified_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="验证时间"
    )