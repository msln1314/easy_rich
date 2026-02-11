#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/7/7 13:41
# @File           : role.py
# @IDE            : PyCharm
# @desc           : 角色模型

from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, Boolean, Integer
from .menu import SysMenu
from .m2m import sys_role_menu,sys_user_role


class SysRole(BaseModel):
    __tablename__ = "sys_role"
    __table_args__ = ({'comment': '角色表'})

    name: Mapped[str] = mapped_column(String(50), index=True, comment="名称")
    code: Mapped[str] = mapped_column(String(50), index=True, comment="权限字符")
    data_range: Mapped[int] = mapped_column(Integer, default=4, comment="数据权限范围")
    status: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否启用")
    order: Mapped[int | None] = mapped_column(Integer, comment="排序")
    remark: Mapped[str | None] = mapped_column(String(255), comment="描述")
    is_admin: Mapped[bool] = mapped_column(Boolean, comment="是否为超级角色", default=False,nullable=True)
    menus: Mapped[set[SysMenu]] = relationship(secondary=sys_role_menu)
    users: Mapped[set['SysUser']] = relationship(secondary=sys_user_role)

