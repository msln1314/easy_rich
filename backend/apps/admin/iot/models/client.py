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

from .client_group import IotClientGroup
from typing import Optional
from .device import IotDevice


class IotClient(BaseModel):
    __tablename__ = "iot_client"
    __table_args__ = ({'comment': '设备表'})

    name: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="名称")
    sn: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="充电桩桩号")
    client_type: Mapped[str] = mapped_column(String(255), nullable=True, comment="类型 充电桩")
    client_tag: Mapped[str] = mapped_column(String(255), nullable=True, comment="类型 交流电 直流电")
    area: Mapped[str] = mapped_column(String(255), nullable=True, comment="区域")
    address: Mapped[str] = mapped_column(String(255), nullable=True, comment="地址")
    is_active: Mapped[int] = mapped_column(Integer, default=1, comment="是否可用")

    group_id: Mapped[Optional[int]] = mapped_column(ForeignKey("iot_client_group.id"))
    group: Mapped[IotClientGroup] = relationship(back_populates="group_clients")

    device_id: Mapped[Optional[int]] = mapped_column(ForeignKey("iot_device.id"))
    device: Mapped[IotDevice] = relationship(back_populates="device_clients")

    connect_type: Mapped[str] = mapped_column(String(255), nullable=True, comment="连接类型")
    port: Mapped[str] = mapped_column(String(255), nullable=True, comment="端口")
    connect_protocol = mapped_column(String(255), nullable=True, comment="连接协议")
    connect_model = mapped_column(String(255), nullable=True, comment="连接模式")
    port_status: Mapped[int] = mapped_column(Integer, nullable=True,default=-1, comment="端口状态  0 断开，1 接通 -1 未使用 ")

    bind_status: Mapped[bool] = mapped_column(Integer, default=0, comment="绑定状态 0 未处置，1  已绑定")
    bind_time: Mapped[datetime | None] = mapped_column(DateTime, comment="绑定时间")
    deal_time: Mapped[datetime | None] = mapped_column(DateTime, comment="处置时间")
    deal_status: Mapped[int] = mapped_column(Integer, default=-1,
                                             comment="处置状态 0 未处置，1 已处置 2 处置中 3 忽略 4 ")
    remark: Mapped[str] = mapped_column(String(255), nullable=True, comment="备注")
