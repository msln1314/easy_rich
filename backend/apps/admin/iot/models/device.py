#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/7/7 13:41
# @File           : user.py
# @IDE            : PyCharm
# @desc           : 用户模型

from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, Boolean, DateTime,Integer,ForeignKey
from typing import Optional
from .product import IotProduct
from apps.admin.log.models.action import SysActionLog

class IotDevice(BaseModel):
    __tablename__ = "iot_device"
    __table_args__ = ({'comment': '设备表 科星'})
    mac: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="mac地址")
    device_type: Mapped[str] = mapped_column(String(255), nullable=True, comment="类型  继电器 网络iO")
    device_tag: Mapped[str] = mapped_column(String(255), nullable=True, comment="类型 ")
    product_id: Mapped[Optional[int]] = mapped_column(ForeignKey("iot_product.id"))
    product: Mapped[IotProduct] = relationship(back_populates="devices")

    area: Mapped[str] = mapped_column(String(255), nullable=True, comment="区域")
    address: Mapped[str] = mapped_column(String(255), nullable=True, comment="地址")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否可用")
    ip: Mapped[str] = mapped_column(String(255), nullable=True, comment="ip地址")
    port: Mapped[str] = mapped_column(String(255), nullable=True, comment="端口")
    phone: Mapped[str] = mapped_column(String(255), nullable=True, comment="手机设备")
    keepalive: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="通讯周期")
    ccid: Mapped[str] = mapped_column(String(255), nullable=True, comment="ccid")
    last_time: Mapped[datetime | None] = mapped_column(DateTime, comment="最近一次在线时间")
    connect_time: Mapped[datetime | None] = mapped_column(DateTime, comment="最近一次连接时间")
    check_time: Mapped[datetime | None] = mapped_column(DateTime, comment="最近一次检查时间")
    deal_status: Mapped[bool] = mapped_column(Boolean, default=False, comment="处置状态 0 未处置，1 已处置 2 处置中 3 忽略 4 ")
    deal_time: Mapped[datetime | None] = mapped_column(DateTime, comment="处置时间")
    remark: Mapped[str] = mapped_column(String(255), nullable=True, comment="备注")

    device_logs: Mapped[list[SysActionLog]] = relationship(back_populates="device")
    device_clients: Mapped[list["IotClient"]] = relationship(back_populates="device")
    device_ports: Mapped[list["IotDevicePort"]] = relationship(back_populates="device")

