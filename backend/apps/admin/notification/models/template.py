# -*- coding: utf-8 -*-
"""通知模板模型"""
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Text
from db.db_base import BaseModel


class NotificationTemplate(BaseModel):
    """通知模板表"""
    __tablename__ = "notification_template"
    __table_args__ = {"comment": "通知模板表"}

    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="模板名称")
    code: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, comment="模板编码"
    )
    title_template: Mapped[str] = mapped_column(
        String(200), nullable=False, comment="标题模板"
    )
    content_template: Mapped[str] = mapped_column(
        Text, nullable=False, comment="内容模板(支持变量插值)"
    )
    channel_types: Mapped[list | None] = mapped_column(
        Text, nullable=True, comment="支持的渠道类型JSON"
    )
    is_system: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="是否系统内置"
    )
    description: Mapped[str | None] = mapped_column(
        String(500), nullable=True, comment="模板描述"
    )