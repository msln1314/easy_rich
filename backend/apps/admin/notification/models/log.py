# -*- coding: utf-8 -*-
"""通知日志模型"""
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime, Integer, Text, Index
from db.db_base import BaseModel


class NotificationLog(BaseModel):
    """通知发送日志表"""
    __tablename__ = "notification_log"
    __table_args__ = (
        Index("idx_user_status", "user_id", "status"),
        Index("idx_created_at", "created_at"),
        {"comment": "通知发送日志表"},
    )

    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="用户ID")
    channel_type: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="渠道类型"
    )
    template_code: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="使用的模板编码"
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="通知标题")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="通知内容")
    status: Mapped[str] = mapped_column(
        String(20), default="pending", comment="状态: pending/sent/failed"
    )
    error_msg: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="错误信息"
    )
    sent_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="发送时间"
    )
    extra_data: Mapped[dict | None] = mapped_column(
        Text, nullable=True, comment="额外数据JSON"
    )


class SystemNotification(BaseModel):
    """系统内通知表"""
    __tablename__ = "system_notification"
    __table_args__ = (
        Index("idx_user_read", "user_id", "is_read"),
        Index("idx_user_created", "user_id", "created_at"),
        {"comment": "系统内通知表"},
    )

    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="用户ID")
    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="通知标题")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="通知内容")
    notification_type: Mapped[str] = mapped_column(
        String(50), default="info", comment="通知类型: info/warning/success/error"
    )
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否已读")
    read_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="阅读时间"
    )
    link: Mapped[str | None] = mapped_column(
        String(500), nullable=True, comment="跳转链接"
    )
    extra_data: Mapped[dict | None] = mapped_column(
        Text, nullable=True, comment="额外数据JSON"
    )