#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/7/7 13:41
# @File           : login.py
# @IDE            : PyCharm
# @desc           : 登录记录模型

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Text
from db.db_base import BaseModel


class SysLoginLog(BaseModel):
    __tablename__ = "sys_login_log"
    __table_args__ = ({'comment': '登录记录表'})

    username: Mapped[str] = mapped_column(String(255), index=True, nullable=False, comment="用户名")
    status: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否登录成功")
    platform: Mapped[str] = mapped_column(String(8), comment="登陆平台")
    login_method: Mapped[str] = mapped_column(String(8), comment="认证方式")
    ip: Mapped[str | None] = mapped_column(String(50), comment="登陆地址")
    address: Mapped[str | None] = mapped_column(String(255), comment="登陆地点")
    country: Mapped[str | None] = mapped_column(String(255), comment="国家")
    province: Mapped[str | None] = mapped_column(String(255), comment="县")
    city: Mapped[str | None] = mapped_column(String(255), comment="城市")
    county: Mapped[str | None] = mapped_column(String(255), comment="区/县")
    operator: Mapped[str | None] = mapped_column(String(255), comment="运营商")
    postal_code: Mapped[str | None] = mapped_column(String(255), comment="邮政编码")
    area_code: Mapped[str | None] = mapped_column(String(255), comment="地区区号")
    browser: Mapped[str | None] = mapped_column(String(50), comment="浏览器")
    system: Mapped[str | None] = mapped_column(String(50), comment="操作系统")
    response: Mapped[str | None] = mapped_column(Text, comment="响应信息")
    request: Mapped[str | None] = mapped_column(Text, comment="请求信息")
