#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/7/7 13:41
# @File           : m2m.py
# @IDE            : PyCharm
# @desc           : 关联中间表

from db.db_base import Base
from sqlalchemy import ForeignKey, Column, Table, Integer


sys_user_role = Table(
    "sys_user_role",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("sys_user.id", ondelete="CASCADE")),
    Column("role_id", Integer, ForeignKey("sys_role.id", ondelete="CASCADE")),
)


sys_user_group = Table(
    "sys_user_group",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("sys_user.id", ondelete="CASCADE")),
    Column("group_id", Integer, ForeignKey("iot_client_group.id", ondelete="CASCADE")),
)


sys_role_menu = Table(
    "sys_role_menu",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("sys_role.id", ondelete="CASCADE")),
    Column("menu_id", Integer, ForeignKey("sys_menu.id", ondelete="CASCADE")),
)

# sys_user_depts = Table(
#     "sys_user_depts",
#     Base.metadata,
#     Column("user_id", Integer, ForeignKey("sys_user.id", ondelete="CASCADE")),
#     Column("dept_id", Integer, ForeignKey("sys_dept.id", ondelete="CASCADE")),
# )
#
# sys_role_depts = Table(
#     "sys_role_depts",
#     Base.metadata,
#     Column("role_id", Integer, ForeignKey("sys_role.id", ondelete="CASCADE")),
#     Column("dept_id", Integer, ForeignKey("sys_dept.id", ondelete="CASCADE")),
# )

