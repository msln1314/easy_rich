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

from typing import Optional
class IotDevicePort(BaseModel):
    __tablename__ = "iot_device_port"
    __table_args__ = ({'comment': '设备端口'})

    name: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="分组名称")
    status: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否禁用")
    remark: Mapped[str | None] = mapped_column(String(255), comment="描述")
    device_id: Mapped[Optional[int]] = mapped_column(ForeignKey("iot_device.id"))
    device: Mapped['IotDevice'] = relationship(back_populates="device_ports")


