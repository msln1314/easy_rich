#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/7/7 13:41
# @File           : user.py
# @IDE            : PyCharm
# @desc           : 系统字典模型

from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer


class SysDictType(BaseModel):
    __tablename__ = "sys_dict_type"
    __table_args__ = ({'comment': '字典类型表'})

    dict_name: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="字典名称")
    dict_type: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="字典类型")
    status: Mapped[bool] = mapped_column(Boolean, default=True, comment="字典状态，是否启用")
    remark: Mapped[str | None] = mapped_column(String(255), comment="备注")
    dicts: Mapped[list["SysDict"]] = relationship(back_populates="dict_type")


class SysDict(BaseModel):
    __tablename__ = "sys_dict"
    __table_args__ = ({'comment': '字典详情表'})

    label: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="字典标签")
    value: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="字典键值")
    color_type: Mapped[str] = mapped_column(String(50), index=True, nullable=True, comment="颜色类型")
    status: Mapped[bool] = mapped_column(Boolean, default=False, comment="字典状态，是否禁用")
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否默认")
    order: Mapped[int] = mapped_column(Integer, comment="字典排序")
    dict_type_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_dict_type.id", ondelete='CASCADE'),
        comment="关联字典类型"
    )
    dict_type: Mapped[SysDictType] = relationship(foreign_keys=dict_type_id, back_populates="dicts")
    remark: Mapped[str | None] = mapped_column(String(255), comment="备注")
