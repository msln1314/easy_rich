#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/7/7 13:41
# @File           : login.py
# @IDE            : PyCharm
# @desc           : 登录记录模型
import json

from sqlalchemy.orm import Mapped, mapped_column

from application.settings import settings
from apps.admin.log.schemas.operation import OperationLog
from utils.ip_manage import IPManage
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_base import BaseModel
from sqlalchemy import String, Boolean, Text,Integer
from fastapi import Request
from starlette.requests import Request as StarletteRequest
from user_agents import parse


class SysOpertationLog(BaseModel):
    __tablename__ = "sys_operation_log"
    __table_args__ = ({'comment': '登录记录表'})



    phone: Mapped[str] = mapped_column(String(255), index=True, nullable=False, comment="手机号")
    user_id: Mapped[int] = mapped_column(Integer, comment="是否登录成功")
    user_name: Mapped[str] = mapped_column(String(8), comment="用户名")
    status_code: Mapped[str] = mapped_column(String(8), comment="认证方式")
    request_api:Mapped[str] = mapped_column(String(8), comment="认证方式")
    content_length:Mapped[Integer] = mapped_column(Integer ,comment="认证方式")
    client_ip: Mapped[str | None] = mapped_column(String(50), comment="登陆地址")
    request_method: Mapped[str | None] = mapped_column(String(255), comment="登陆地点")
    api_path: Mapped[str | None] = mapped_column(String(255), comment="国家")
    summary: Mapped[str | None] = mapped_column(String(255), comment="信息")
    route_name: Mapped[str | None] = mapped_column(String(255), comment="路由名称")
    description: Mapped[str | None] = mapped_column(String(255), comment="描述")
    tags: Mapped[str | None] = mapped_column(String(255), comment="标签")
    browser: Mapped[str | None] = mapped_column(String(50), comment="浏览器")
    system: Mapped[str | None] = mapped_column(String(50), comment="操作系统")
    process_time: Mapped[float | None] = mapped_column(Text, comment="响应时间")
    params: Mapped[str | None] = mapped_column(Text, comment="请求参数")

    @classmethod
    async def create_operation_log(
            cls,
            db: AsyncSession,
            data: dict,
            status: bool,
            req: Request | StarletteRequest,
            resp: dict
    ):
        """
        创建登录记录
        :return:
        """
        if not settings.OPERATION_LOG_RECORD:
            return None
        print(data,"data")
        obj = SysOpertationLog(
            **data
        )
        db.add(obj)
        await db.flush()
        await db.commit()
        print("88989")
