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
from .product_cate import IotProductCate


class IotProduct(BaseModel):
    __tablename__ = "iot_product"
    __table_args__ = ({'comment': '产品设备表'})

    name: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="产品名称")
    product_type: Mapped[str] = mapped_column(String(255), nullable=True, comment="类型 充电桩 网关")
    product_tag: Mapped[str] = mapped_column(String(255), nullable=True, comment="类型  直流电")
    # area: Mapped[str] = mapped_column(String(255), nullable=True, comment="区域")
    # address: Mapped[str] = mapped_column(String(255), nullable=True, comment="地址")
    devices: Mapped[list["IotDevice"]] = relationship(back_populates="product")

    connect_type: Mapped[str] = mapped_column(String(255), nullable=True, comment="连接类型")
    remark: Mapped[str] = mapped_column(String(255), nullable=True, comment="备注")

    cate_id: Mapped[Optional[int]] = mapped_column(ForeignKey("iot_product_cate.id"))
    cate: Mapped[IotProductCate] = relationship(back_populates="cate_products")
