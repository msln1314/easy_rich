#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/02/08
# @File           : sys_user_stock_group.py
# @IDE            : PyCharm
# @desc           : 用户股票分组关联模型

from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base
from sqlalchemy import Integer, Index, ForeignKey
from sqlalchemy import DateTime, func
from datetime import datetime

class SysUserStockGroup(Base):
    __tablename__ = "sys_user_stock_group"
    __table_args__ = (
        Index('idx_group_id', 'group_id'),
        Index('idx_user_id', 'user_id'),
        {'comment': '用户股票分组关联表'}
    )
    id:  Mapped[int] = mapped_column(Integer, primary_key=True, comment='主键ID')
    user_id:  Mapped[int | None] = mapped_column(Integer, ForeignKey('sys_user.id', ondelete="CASCADE", onupdate="RESTRICT"), nullable=True, comment="用户ID")
    group_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('stock_group.id', ondelete="CASCADE", onupdate="RESTRICT"), nullable=True, comment="分组ID")
    stock_id:  Mapped[int | None] = mapped_column(Integer, nullable=True, comment="股票ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        comment='更新时间'
    )
