#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/10/23 13:41
# @File           : dept.py
# @IDE            : PyCharm
# @desc           : 设备分组模型

from sqlalchemy.orm import Mapped, mapped_column,relationship
from db.db_base import BaseModel
from sqlalchemy import String, Boolean, Integer, ForeignKey


class IotClientGroup(BaseModel):
    __tablename__ = "iot_client_group"
    __table_args__ = ({'comment': '客户端分组'})

    name: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="分组名称")
    status: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否启用")
    order: Mapped[int | None] = mapped_column(Integer, comment="显示排序")
    remark: Mapped[str | None] = mapped_column(String(255), comment="描述")


    parent_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("iot_client_group.id", ondelete='CASCADE'),
        comment="上级分组"
    )
    group_clients: Mapped[list["IotClient"]] = relationship(back_populates="group")
