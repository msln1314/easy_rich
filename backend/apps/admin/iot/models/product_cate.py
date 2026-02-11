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


class IotProductCate(BaseModel):
    __tablename__ = "iot_product_cate"
    __table_args__ = ({'comment': '产品分类表'})

    name: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="名称")
    status: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否禁用")
    order: Mapped[int | None] = mapped_column(Integer, comment="显示排序")
    remark: Mapped[str | None] = mapped_column(String(255), comment="描述")
    cate_products: Mapped[list["IotProduct"]] = relationship(back_populates="cate")
