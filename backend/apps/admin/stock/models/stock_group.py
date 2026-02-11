#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/02/08
# @File           : stock_group.py
# @IDE            : PyCharm
# @desc           : 股票分组模型

from sqlalchemy.orm import Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, DateTime, Integer, Index, ForeignKey


class StockGroup(BaseModel):
    __tablename__ = "stock_group"
    __table_args__ = (
        Index('idx_parent_id', 'parent_id'),
        Index('idx_name', 'name'),
        {'comment': '股票分组'}
    )

    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="分组名称")
    status: Mapped[int] = mapped_column(Integer, nullable=False, comment="是否禁用")
    order: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="显示排序")
    remark: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="描述")
    parent_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('stock_group.id', ondelete="CASCADE", onupdate="RESTRICT"), nullable=True, comment="上级分组")
    user_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="用户ID")
